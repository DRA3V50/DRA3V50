#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

USERNAME = os.getenv("PROFILE_USERNAME", "DRA3V50")
OUTPUT = Path(os.getenv("CARD_OUTPUT", "assets/security-research-diagnostics.svg"))
EASTERN = ZoneInfo("America/New_York")
API_ROOT = "https://api.github.com"


def github_json(path: str):
    token = os.getenv("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dynamic-security-diagnostics-card",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers=headers,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_github_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_eastern(instant: datetime | None) -> tuple[str, str]:
    if instant is None:
        return "NO PUBLIC", "ACTIVITY"

    local = instant.astimezone(EASTERN)
    hour = local.strftime("%I").lstrip("0") or "0"
    return (
        local.strftime("%b %d").upper(),
        f"{hour}:{local.strftime('%M %p %Z')}",
    )


def load_activity() -> dict:
    events = []

    for page in range(1, 4):
        batch = github_json(
            f"/users/{USERNAME}/events/public?per_page=100&page={page}"
        )

        if not isinstance(batch, list) or not batch:
            break

        events.extend(batch)

        if len(batch) < 100:
            break

    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    parsed = []
    for event in events:
        created = parse_github_time(event.get("created_at"))
        if created is not None:
            parsed.append((created, event))

    parsed.sort(key=lambda item: item[0], reverse=True)

    events_7d = sum(
        1 for created, _ in parsed if created >= seven_days_ago
    )

    commits_7d = 0
    repos_30d = set()

    for created, event in parsed:
        if created >= thirty_days_ago:
            repo = event.get("repo", {}).get("name")
            if repo:
                repos_30d.add(repo)

        if created >= seven_days_ago and event.get("type") == "PushEvent":
            payload = event.get("payload", {})
            size = payload.get("size")

            if isinstance(size, int):
                commits_7d += size
            else:
                commits = payload.get("commits", [])
                if isinstance(commits, list):
                    commits_7d += len(commits)

    last_activity = parsed[0][0] if parsed else None

    return {
        "events_7d": events_7d,
        "commits_7d": commits_7d,
        "repos_30d": len(repos_30d),
        "last_activity": last_activity,
    }


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_svg(metrics: dict) -> str:
    last_date, last_time = format_eastern(metrics["last_activity"])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="180" viewBox="0 0 400 180">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#171927"/>
      <stop offset="100%" stop-color="#101522"/>
    </linearGradient>
    <linearGradient id="header" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#245b85"/>
      <stop offset="100%" stop-color="#173b62"/>
    </linearGradient>
  </defs>

  <rect x="1" y="1" width="398" height="178" rx="12" fill="url(#bg)" stroke="#536f91" stroke-width="2"/>
  <rect x="1" y="1" width="398" height="38" rx="12" fill="url(#header)"/>
  <rect x="1" y="28" width="398" height="11" fill="#173b62"/>

  <text x="200" y="25" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="16" font-weight="700" fill="#eef6ff">
    Integrated Security Research &amp; Diagnostics
  </text>

  <text x="68" y="57" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="9" font-weight="700" fill="#7aa2f7">INGEST</text>

  <path d="M22 76 H56" stroke="#bb9af7" stroke-width="4" stroke-linecap="round"/>
  <path d="M22 96 H56" stroke="#70a5fd" stroke-width="4" stroke-linecap="round"/>
  <path d="M22 116 H56" stroke="#38bdae" stroke-width="4" stroke-linecap="round"/>
  <path d="M56 76 L78 89" stroke="#bb9af7" stroke-width="4" stroke-linecap="round"/>
  <path d="M56 96 H78" stroke="#70a5fd" stroke-width="4" stroke-linecap="round"/>
  <path d="M56 116 L78 103" stroke="#38bdae" stroke-width="4" stroke-linecap="round"/>
  <polygon points="76,88 90,96 76,104" fill="#70a5fd"/>

  <text x="58" y="136" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="10" font-weight="700" fill="#dbe8f7">{esc(metrics["events_7d"])} EVENTS</text>
  <text x="58" y="149" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="8" fill="#8199b5">LAST 7 DAYS</text>

  <text x="200" y="57" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="9" font-weight="700" fill="#7aa2f7">ANALYZE</text>

  <rect x="164" y="68" width="72" height="62" rx="9" fill="#18293a"
        stroke="#70a5fd" stroke-width="2"/>

  <g stroke="#607c9e" stroke-width="3" stroke-linecap="round">
    <path d="M176 62 V68"/><path d="M188 62 V68"/><path d="M200 62 V68"/>
    <path d="M212 62 V68"/><path d="M224 62 V68"/>
    <path d="M176 130 V136"/><path d="M188 130 V136"/><path d="M200 130 V136"/>
    <path d="M212 130 V136"/><path d="M224 130 V136"/>
    <path d="M158 81 H164"/><path d="M158 93 H164"/><path d="M158 105 H164"/><path d="M158 117 H164"/>
    <path d="M236 81 H242"/><path d="M236 93 H242"/><path d="M236 105 H242"/><path d="M236 117 H242"/>
  </g>

  <circle cx="185" cy="88" r="5" fill="#70a5fd"/>
  <circle cx="211" cy="85" r="5" fill="#38bdae"/>
  <circle cx="214" cy="111" r="6" fill="#9ece6a"/>
  <circle cx="185" cy="113" r="5" fill="#bb9af7"/>
  <circle cx="200" cy="100" r="5" fill="#edf5ff"/>

  <g stroke="#d8e4ef" stroke-width="1.8" fill="none">
    <path d="M185 88 L200 100"/><path d="M211 85 L200 100"/>
    <path d="M214 111 L200 100"/><path d="M185 113 L200 100"/>
  </g>

  <text x="200" y="145" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="9" font-weight="700" fill="#dbe8f7">{esc(metrics["commits_7d"])} COMMITS • {esc(metrics["repos_30d"])} REPOS</text>
  <text x="200" y="157" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="8" fill="#8199b5">7D PUSHES • 30D REPOSITORIES</text>

  <path d="M249 99 H281" stroke="#9ece6a" stroke-width="4" stroke-linecap="round"/>
  <polygon points="280,92 294,99 280,106" fill="#9ece6a"/>

  <text x="334" y="57" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="9" font-weight="700" fill="#7aa2f7">VALIDATE</text>

  <circle cx="327" cy="93" r="27" fill="#18293a" stroke="#8da8c7" stroke-width="3"/>
  <circle cx="327" cy="93" r="18" fill="#112032" stroke="#4e6886" stroke-width="1.5"/>
  <path d="M316 93 L324 101 L340 83" fill="none" stroke="#9ece6a"
        stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M347 113 L365 131" stroke="#8da8c7" stroke-width="8" stroke-linecap="round"/>
  <path d="M347 113 L365 131" stroke="#5d78a0" stroke-width="4" stroke-linecap="round"/>

  <text x="329" y="139" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="9" font-weight="700" fill="#9ece6a">SYNC OK</text>
  <text x="329" y="151" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="8" fill="#dbe8f7">{esc(last_date)}</text>
  <text x="329" y="162" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="8" fill="#8199b5">{esc(last_time)}</text>

  <text x="200" y="174" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="7.5" letter-spacing="0.9" fill="#657f9d">
    BLUE TEAM • FORENSICS • SECURITY RESEARCH
  </text>
</svg>
'''


def main() -> None:
    try:
        metrics = load_activity()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SystemExit(f"GitHub activity retrieval failed: {exc}") from exc

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(metrics), encoding="utf-8")

    print(
        "Dynamic security diagnostics card updated: "
        f"events_7d={metrics['events_7d']}, "
        f"commits_7d={metrics['commits_7d']}, "
        f"repos_30d={metrics['repos_30d']}"
    )


if __name__ == "__main__":
    main()
