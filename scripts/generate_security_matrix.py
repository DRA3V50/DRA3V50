#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

USER = os.getenv("PROFILE_USERNAME", "DRA3V50")
OUT_GIF = Path(
    os.getenv(
        "CARD_OUTPUT_GIF",
        "assets/security-intelligence-matrix.gif",
    )
)
OUT_JSON = Path(
    os.getenv(
        "CARD_OUTPUT_JSON",
        "data/security_matrix.json",
    )
)
TOKEN = os.getenv("GITHUB_TOKEN", "").strip()

ET = ZoneInfo("America/New_York")

W = 820
H = 280

# 20 FPS, 6-second seamless loop.
FRAMES = 120
MS = 50

BG = (10, 14, 24)
PANEL = (18, 25, 40)
EDGE = (72, 190, 220)
EDGE_HOT = (107, 224, 243)
TEXT = (232, 241, 250)
MUTED = (126, 155, 184)
BLUE = (78, 135, 224)
CYAN = (56, 198, 205)
GREEN = (158, 206, 106)
PURPLE = (187, 154, 247)

# Matrix rendering envelope. Keeping these centralized makes it easy to
# guarantee that the rotating geometry never enters the title/footer regions.
MATRIX_CENTER_X = 410
MATRIX_CENTER_Y = 180
MATRIX_SCALE = 29.0
MATRIX_TOP_LIMIT = 65
MATRIX_BOTTOM_LIMIT = 240


def fnt(size: int, bold: bool = False):
    names = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]

    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass

    return ImageFont.load_default()


def api(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "security-intelligence-matrix",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(
        "https://api.github.com" + path,
        headers=headers,
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def dt(value):
    try:
        return datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )
    except (TypeError, ValueError):
        return None


def collect():
    user = api(f"/users/{USER}")
    repos = api(
        f"/users/{USER}/repos?type=owner&sort=updated&per_page=100"
    )
    events = api(
        f"/users/{USER}/events/public?per_page=100"
    )

    repos = (
        [
            repo
            for repo in repos
            if isinstance(repo, dict)
            and not repo.get("fork", False)
        ]
        if isinstance(repos, list)
        else []
    )
    events = events if isinstance(events, list) else []

    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    stars = sum(
        int(repo.get("stargazers_count", 0) or 0)
        for repo in repos
    )

    events_7d = 0

    for event in events:
        created = (
            dt(event.get("created_at"))
            if isinstance(event, dict)
            else None
        )

        if created and created >= seven_days_ago:
            events_7d += 1

    active_repos = sum(
        1
        for repo in repos
        if (
            dt(
                repo.get("pushed_at")
                or repo.get("updated_at")
            )
            or datetime.min.replace(tzinfo=timezone.utc)
        )
        >= thirty_days_ago
    )

    languages = {}

    for repo in repos:
        full_name = repo.get("full_name")

        if not full_name:
            continue

        try:
            data = api(f"/repos/{full_name}/languages")
        except (urllib.error.HTTPError, urllib.error.URLError):
            continue

        if not isinstance(data, dict):
            continue

        for language, amount in data.items():
            try:
                languages[language] = (
                    languages.get(language, 0)
                    + int(amount)
                )
            except (TypeError, ValueError):
                pass

    total_language_bytes = sum(languages.values())
    ranked = sorted(
        languages.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    primary_language = "Unknown"
    primary_pct = 0.0

    if ranked and total_language_bytes:
        primary_language = ranked[0][0]
        primary_pct = round(
            ranked[0][1] * 100 / total_language_bytes,
            1,
        )

    now_et = datetime.now(ET)
    hour = now_et.strftime("%I").lstrip("0") or "0"

    return {
        "public_repos": int(
            user.get("public_repos", len(repos))
            or 0
        ),
        "followers": int(
            user.get("followers", 0)
            or 0
        ),
        "total_stars": stars,
        "events_7d": events_7d,
        "repos_updated_30d": active_repos,
        "primary_language": primary_language,
        "primary_language_pct": primary_pct,
        "status": "SYNC OK",
        "generated_date": now_et.strftime("%b %d").upper(),
        "generated_time": (
            f"{hour}:{now_et.strftime('%M %p %Z')}"
        ),
    }


def rotate_y(point, angle):
    x, y, z = point
    cosine = math.cos(angle)
    sine = math.sin(angle)

    return (
        x * cosine + z * sine,
        y,
        -x * sine + z * cosine,
    )


def rotate_x(point, angle):
    x, y, z = point
    cosine = math.cos(angle)
    sine = math.sin(angle)

    return (
        x,
        y * cosine - z * sine,
        y * sine + z * cosine,
    )


def add(a, b):
    return tuple(
        a[index] + b[index]
        for index in range(3)
    )


def project(
    point,
    center_x=MATRIX_CENTER_X,
    center_y=MATRIX_CENTER_Y,
    scale=MATRIX_SCALE,
):
    x, y, z = point

    camera = 13.0
    factor = camera / max(
        5.0,
        camera - z,
    )

    return (
        center_x + x * scale * factor,
        center_y - y * scale * factor,
    )


VERTICES = [
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
]

FACES = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (1, 2, 6, 5),
    (0, 3, 7, 4),
]


def centers():
    """
    Build a continuous square loop from 20 cube positions.

    The loop is deliberately wider than it is tall in screen projection so it
    reads as a data matrix instead of a stack of cubes.
    """
    values = (
        -3.0,
        -1.8,
        -0.6,
        0.6,
        1.8,
        3.0,
    )

    output = []

    output += [
        (x, 0.0, -3.0)
        for x in values
    ]

    output += [
        (3.0, 0.0, z)
        for z in values[1:-1]
    ]

    output += [
        (x, 0.0, 3.0)
        for x in reversed(values)
    ]

    output += [
        (-3.0, 0.0, z)
        for z in reversed(values[1:-1])
    ]

    return output


def text_center(draw, xy, text, used_font, fill):
    bounds = draw.textbbox(
        (0, 0),
        text,
        font=used_font,
    )

    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]

    draw.text(
        (
            xy[0] - width / 2,
            xy[1] - height / 2,
        ),
        text,
        font=used_font,
        fill=fill,
    )


def cube_points(
    center,
    local_angle,
    global_angle_y,
    global_angle_x,
):
    points = []

    for vertex in VERTICES:
        point = (
            vertex[0] * 0.82,
            vertex[1] * 0.82,
            vertex[2] * 0.82,
        )

        # Each cube has its own CW/CCW spin.
        point = rotate_y(
            point,
            local_angle,
        )

        point = add(
            point,
            center,
        )

        # The complete loop performs one full 360-degree revolution.
        point = rotate_y(
            point,
            global_angle_y,
        )

        point = rotate_x(
            point,
            global_angle_x,
        )

        points.append(point)

    return points


def matrix_geometry(frame_index):
    t = frame_index / FRAMES

    # Exactly one 360-degree revolution per GIF loop.
    global_angle_y = (
        t
        * 2.0
        * math.pi
    )

    # Constant viewing tilt keeps depth visible throughout the turn.
    global_angle_x = math.radians(-27)

    records = []

    for index, center in enumerate(centers()):
        direction = (
            1
            if index % 2 == 0
            else -1
        )

        # Adjacent cubes alternate CW/CCW and also complete a full turn.
        local_angle = (
            index * 0.15
            + direction
            * t
            * 2.0
            * math.pi
        )

        points = cube_points(
            center,
            local_angle,
            global_angle_y,
            global_angle_x,
        )

        average_z = (
            sum(point[2] for point in points)
            / len(points)
        )

        records.append(
            (
                average_z,
                index,
                points,
            )
        )

    records.sort(
        key=lambda item: item[0]
    )

    return records


def geometry_bounds():
    """
    Validate every animation frame before rendering.

    This prevents the cube loop from ever entering the title bar or footer.
    """
    minimum_x = float("inf")
    minimum_y = float("inf")
    maximum_x = float("-inf")
    maximum_y = float("-inf")

    for frame_index in range(FRAMES):
        for _, _, points in matrix_geometry(frame_index):
            for point in points:
                x, y = project(point)

                minimum_x = min(minimum_x, x)
                minimum_y = min(minimum_y, y)
                maximum_x = max(maximum_x, x)
                maximum_y = max(maximum_y, y)

    if minimum_y < MATRIX_TOP_LIMIT:
        raise RuntimeError(
            "Matrix geometry enters the title region: "
            f"top={minimum_y:.2f}, "
            f"limit={MATRIX_TOP_LIMIT}."
        )

    if maximum_y > MATRIX_BOTTOM_LIMIT:
        raise RuntimeError(
            "Matrix geometry enters the footer region: "
            f"bottom={maximum_y:.2f}, "
            f"limit={MATRIX_BOTTOM_LIMIT}."
        )

    if minimum_x < 220 or maximum_x > 600:
        raise RuntimeError(
            "Matrix geometry entered a side-metric region: "
            f"x={minimum_x:.2f}..{maximum_x:.2f}."
        )

    return (
        minimum_x,
        minimum_y,
        maximum_x,
        maximum_y,
    )


def frame(data, frame_index):
    image = Image.new(
        "RGB",
        (W, H),
        BG,
    )

    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (8, 8, W - 8, H - 8),
        22,
        fill=PANEL,
        outline=(60, 94, 132),
        width=3,
    )

    draw.rounded_rectangle(
        (8, 8, W - 8, 60),
        22,
        fill=(28, 69, 105),
    )

    draw.rectangle(
        (8, 40, W - 8, 60),
        fill=(20, 53, 86),
    )

    text_center(
        draw,
        (W / 2, 34),
        "INTEGRATED SECURITY INTELLIGENCE MATRIX",
        fnt(23, True),
        TEXT,
    )

    # LEFT COLUMN
    draw.text(
        (28, 83),
        "PUBLIC ACTIVITY",
        font=fnt(11, True),
        fill=BLUE,
    )

    draw.text(
        (28, 105),
        f"{data['events_7d']} EVENTS",
        font=fnt(22, True),
        fill=TEXT,
    )

    draw.text(
        (28, 132),
        "LAST 7 DAYS",
        font=fnt(9),
        fill=MUTED,
    )

    draw.text(
        (28, 173),
        "ACTIVE REPOSITORIES",
        font=fnt(11, True),
        fill=BLUE,
    )

    draw.text(
        (28, 195),
        f"{data['repos_updated_30d']} UPDATED",
        font=fnt(22, True),
        fill=TEXT,
    )

    draw.text(
        (28, 222),
        "LAST 30 DAYS",
        font=fnt(9),
        fill=MUTED,
    )

    # RIGHT COLUMN
    draw.text(
        (642, 83),
        "PROFILE SIGNAL",
        font=fnt(11, True),
        fill=BLUE,
    )

    draw.text(
        (642, 105),
        f"{data['total_stars']} STARS",
        font=fnt(22, True),
        fill=TEXT,
    )

    draw.text(
        (642, 135),
        f"{data['followers']} FOLLOWERS",
        font=fnt(14, True),
        fill=TEXT,
    )

    draw.text(
        (642, 173),
        "VALIDATION",
        font=fnt(11, True),
        fill=BLUE,
    )

    draw.text(
        (642, 195),
        data["status"],
        font=fnt(18, True),
        fill=GREEN,
    )

    draw.text(
        (642, 222),
        (
            f"{data['generated_date']}  "
            f"{data['generated_time']}"
        ),
        font=fnt(9),
        fill=MUTED,
    )

    records = matrix_geometry(frame_index)
    projected_centers = {}

    # Depth-sort cubes.
    for _, index, points_3d in records:
        face_records = []

        for face_index, face in enumerate(FACES):
            face_points = [
                points_3d[position]
                for position in face
            ]

            average_z = (
                sum(point[2] for point in face_points)
                / len(face_points)
            )

            face_records.append(
                (
                    average_z,
                    face_index,
                    face_points,
                )
            )

        face_records.sort(
            key=lambda item: item[0]
        )

        # Draw depth-sorted cube faces.
        for _, face_index, face_points in face_records:
            polygon = [
                project(point)
                for point in face_points
            ]

            if face_index in (1, 4):
                fill = (19, 52, 74)
            elif face_index in (2, 3):
                fill = (17, 43, 64)
            else:
                fill = (14, 34, 53)

            draw.polygon(
                polygon,
                fill=fill,
                outline=EDGE,
            )

        center_3d = tuple(
            sum(
                points_3d[vertex][axis]
                for vertex in range(8)
            )
            / 8
            for axis in range(3)
        )

        projected_centers[index] = project(
            center_3d
        )

    # Slowly moving scan highlight across the loop.
    hot_index = int(
        (
            frame_index
            / FRAMES
        )
        * len(projected_centers)
    ) % len(projected_centers)

    hot_position = projected_centers.get(
        hot_index
    )

    if hot_position:
        draw.ellipse(
            (
                hot_position[0] - 7,
                hot_position[1] - 7,
                hot_position[0] + 7,
                hot_position[1] + 7,
            ),
            outline=EDGE_HOT,
            width=2,
        )

    anchors = [
        (
            0,
            str(data["public_repos"]),
            "REPOS",
            CYAN,
        ),
        (
            5,
            str(data["total_stars"]),
            "STARS",
            PURPLE,
        ),
        (
            10,
            f"{data['primary_language_pct']:.0f}%",
            data["primary_language"].upper(),
            BLUE,
        ),
        (
            15,
            "OK",
            "SYNC",
            GREEN,
        ),
    ]

    for index, value, label, color in anchors:
        position = projected_centers[index]
        x, y = position

        draw.ellipse(
            (
                x - 21,
                y - 17,
                x + 21,
                y + 17,
            ),
            fill=(10, 22, 35),
            outline=color,
            width=2,
        )

        text_center(
            draw,
            (x, y - 3),
            value,
            fnt(10, True),
            TEXT,
        )

        text_center(
            draw,
            (x, y + 9),
            label,
            fnt(6, True),
            color,
        )

    # Footer, intentionally outside the validated matrix region.
    draw.line(
        (
            28,
            246,
            W - 28,
            246,
        ),
        fill=(40, 62, 88),
        width=1,
    )

    text_center(
        draw,
        (W / 2, 261),
        (
            "BLUE TEAM  •  DIGITAL FORENSICS  •  "
            "CYBER INTELLIGENCE  •  DATA ANALYSIS"
        ),
        fnt(9),
        MUTED,
    )

    return image


def build_shared_palette(frames):
    """
    Build one deterministic GIF palette and use it for every frame.

    This avoids per-frame palette shimmer while the cubes rotate.
    """
    sample = Image.new(
        "RGB",
        (
            W,
            H * min(8, len(frames)),
        ),
        BG,
    )

    for index, source in enumerate(
        frames[
            :: max(
                1,
                len(frames) // 8,
            )
        ][:8]
    ):
        sample.paste(
            source,
            (
                0,
                index * H,
            ),
        )

    return sample.quantize(
        colors=128,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )


def quantize_frames(frames):
    palette_source = build_shared_palette(
        frames
    )

    palette = palette_source.getpalette()

    quantized = []

    for source in frames:
        frame_p = source.quantize(
            palette=palette_source,
            dither=Image.Dither.NONE,
        )

        # Explicitly retain the same global palette.
        frame_p.putpalette(palette)

        quantized.append(frame_p)

    return quantized


def render(data):
    bounds = geometry_bounds()

    print(
        "Validated matrix bounds: "
        f"x={bounds[0]:.1f}..{bounds[2]:.1f}, "
        f"y={bounds[1]:.1f}..{bounds[3]:.1f}"
    )

    raw_frames = [
        frame(
            data,
            frame_index,
        )
        for frame_index in range(FRAMES)
    ]

    frames = quantize_frames(
        raw_frames
    )

    OUT_GIF.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=MS,
        loop=0,
        disposal=2,
        optimize=False,
    )


def main():
    data = collect()

    OUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_JSON.write_text(
        json.dumps(
            data,
            indent=2,
        ),
        encoding="utf-8",
    )

    render(data)

    print(
        json.dumps(
            data,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
