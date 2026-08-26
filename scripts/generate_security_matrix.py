#!/usr/bin/env python3
from __future__ import annotations
import json, math, os, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

USER=os.getenv('PROFILE_USERNAME','DRA3V50')
OUT_GIF=Path(os.getenv('CARD_OUTPUT_GIF','assets/security-intelligence-matrix.gif'))
OUT_JSON=Path(os.getenv('CARD_OUTPUT_JSON','data/security_matrix.json'))
TOKEN=os.getenv('GITHUB_TOKEN','').strip()
ET=ZoneInfo('America/New_York')
W,H=820,280
FRAMES=48
MS=100

BG=(10,14,24); PANEL=(18,25,40); EDGE=(72,190,220); TEXT=(232,241,250); MUTED=(126,155,184)
BLUE=(78,135,224); CYAN=(56,198,205); GREEN=(158,206,106); PURPLE=(187,154,247)

def fnt(size,bold=False):
    names=['DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for n in names:
        try:return ImageFont.truetype(n,size)
        except OSError:pass
    return ImageFont.load_default()

def api(path):
    hdr={'Accept':'application/vnd.github+json','User-Agent':'security-intelligence-matrix','X-GitHub-Api-Version':'2022-11-28'}
    if TOKEN: hdr['Authorization']=f'Bearer {TOKEN}'
    req=urllib.request.Request('https://api.github.com'+path,headers=hdr)
    with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read().decode())

def dt(v):
    try:return datetime.fromisoformat(str(v).replace('Z','+00:00'))
    except:return None

def collect():
    user=api(f'/users/{USER}')
    repos=api(f'/users/{USER}/repos?type=owner&sort=updated&per_page=100')
    events=api(f'/users/{USER}/events/public?per_page=100')
    repos=[r for r in repos if isinstance(r,dict) and not r.get('fork',False)] if isinstance(repos,list) else []
    events=events if isinstance(events,list) else []
    now=datetime.now(timezone.utc); d7=now-timedelta(days=7); d30=now-timedelta(days=30)
    stars=sum(int(r.get('stargazers_count',0) or 0) for r in repos)
    ev7=0
    for e in events:
        t=dt(e.get('created_at')) if isinstance(e,dict) else None
        if t and t>=d7: ev7+=1
    active=sum(1 for r in repos if (dt(r.get('pushed_at') or r.get('updated_at')) or datetime.min.replace(tzinfo=timezone.utc))>=d30)
    langs={}
    for r in repos:
        name=r.get('full_name')
        if not name:continue
        try: data=api(f'/repos/{name}/languages')
        except Exception: continue
        if isinstance(data,dict):
            for k,v in data.items():
                try:langs[k]=langs.get(k,0)+int(v)
                except:pass
    total=sum(langs.values()); ranked=sorted(langs.items(),key=lambda x:x[1],reverse=True)
    lang='Unknown'; pct=0.0
    if ranked and total:
        lang=ranked[0][0]; pct=round(ranked[0][1]*100/total,1)
    nowet=datetime.now(ET); hour=nowet.strftime('%I').lstrip('0') or '0'
    return {'public_repos':int(user.get('public_repos',len(repos)) or 0),'followers':int(user.get('followers',0) or 0),'total_stars':stars,'events_7d':ev7,'repos_updated_30d':active,'primary_language':lang,'primary_language_pct':pct,'status':'SYNC OK','generated_date':nowet.strftime('%b %d').upper(),'generated_time':f"{hour}:{nowet.strftime('%M %p %Z')}"}

def ry(p,a):
    x,y,z=p;c=math.cos(a);s=math.sin(a);return(x*c+z*s,y,-x*s+z*c)
def rx(p,a):
    x,y,z=p;c=math.cos(a);s=math.sin(a);return(x,y*c-z*s,y*s+z*c)
def add(a,b):return tuple(a[i]+b[i] for i in range(3))
def proj(p,cx=410,cy=170,scale=37):
    x,y,z=p;cam=12;fac=cam/max(4,cam-z);return(cx+x*scale*fac,cy-y*scale*fac)

VERT=[(-.5,-.5,-.5),(.5,-.5,-.5),(.5,.5,-.5),(-.5,.5,-.5),(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)]
FACES=[(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(1,2,6,5),(0,3,7,4)]

def centers():
    vals=(-3,-1.8,-.6,.6,1.8,3); out=[]
    out += [(x,0,-3) for x in vals]
    out += [(3,0,z) for z in vals[1:-1]]
    out += [(x,0,3) for x in reversed(vals)]
    out += [(-3,0,z) for z in reversed(vals[1:-1])]
    return out

def text_center(draw,xy,s,font,fill):
    b=draw.textbbox((0,0),s,font=font); draw.text((xy[0]-(b[2]-b[0])/2,xy[1]-(b[3]-b[1])/2),s,font=font,fill=fill)

def frame(data,i):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((8,8,W-8,H-8),22,fill=PANEL,outline=(60,94,132),width=3)
    d.rounded_rectangle((8,8,W-8,60),22,fill=(28,69,105));d.rectangle((8,40,W-8,60),fill=(20,53,86))
    text_center(d,(W/2,34),'INTEGRATED SECURITY INTELLIGENCE MATRIX',fnt(23,True),TEXT)
    d.text((28,83),'PUBLIC ACTIVITY',font=fnt(11,True),fill=BLUE);d.text((28,105),f"{data['events_7d']} EVENTS",font=fnt(22,True),fill=TEXT);d.text((28,132),'LAST 7 DAYS',font=fnt(9),fill=MUTED)
    d.text((28,173),'ACTIVE REPOSITORIES',font=fnt(11,True),fill=BLUE);d.text((28,195),f"{data['repos_updated_30d']} UPDATED",font=fnt(22,True),fill=TEXT);d.text((28,222),'LAST 30 DAYS',font=fnt(9),fill=MUTED)
    d.text((642,83),'PROFILE SIGNAL',font=fnt(11,True),fill=BLUE);d.text((642,105),f"{data['total_stars']} STARS",font=fnt(22,True),fill=TEXT);d.text((642,135),f"{data['followers']} FOLLOWERS",font=fnt(14,True),fill=TEXT)
    d.text((642,173),'VALIDATION',font=fnt(11,True),fill=BLUE);d.text((642,195),data['status'],font=fnt(18,True),fill=GREEN);d.text((642,222),f"{data['generated_date']}  {data['generated_time']}",font=fnt(9),fill=MUTED)
    t=i/FRAMES; gy=math.radians(31)+math.sin(t*2*math.pi)*math.radians(10); gx=math.radians(-24)
    rec=[]
    for idx,c in enumerate(centers()):
        local=(1 if idx%2==0 else -1)*(t*2*math.pi+idx*.12)
        pts=[]
        for v in VERT:
            p=(v[0]*.8,v[1]*.8,v[2]*.8);p=ry(p,local);p=add(p,c);p=ry(p,gy);p=rx(p,gx);pts.append(p)
        rec.append((sum(p[2] for p in pts)/8,idx,pts))
    rec.sort(key=lambda x:x[0]); pc={}
    for _,idx,pts3 in rec:
        faces=[]
        for fi,face in enumerate(FACES):
            q=[pts3[j] for j in face];faces.append((sum(p[2] for p in q)/4,fi,q))
        faces.sort(key=lambda x:x[0])
        for _,fi,q in faces:
            poly=[proj(p) for p in q];fill=(15,35,54) if fi in (0,5) else (19,48,69) if fi in (1,4) else (17,42,62)
            d.polygon(poly,fill=fill,outline=EDGE)
        c3=tuple(sum(pts3[j][a] for j in range(8))/8 for a in range(3));pc[idx]=proj(c3)
    anchors=[(0,str(data['public_repos']),'REPOS',CYAN),(5,str(data['total_stars']),'STARS',PURPLE),(10,f"{data['primary_language_pct']:.0f}%",data['primary_language'].upper(),BLUE),(15,'OK','SYNC',GREEN)]
    for idx,val,lab,col in anchors:
        x,y=pc[idx];d.ellipse((x-22,y-18,x+22,y+18),fill=(10,22,35),outline=col,width=2);text_center(d,(x,y-3),val,fnt(11,True),TEXT);text_center(d,(x,y+10),lab,fnt(7,True),col)
    text_center(d,(410,169),'ROTATING DATA LOOP',fnt(10,True),(175,201,225))
    d.line((28,246,W-28,246),fill=(40,62,88),width=1);text_center(d,(W/2,261),'BLUE TEAM  •  DIGITAL FORENSICS  •  CYBER INTELLIGENCE  •  DATA ANALYSIS',fnt(9),MUTED)
    return im

def render(data):
    frames=[frame(data,i) for i in range(FRAMES)];OUT_GIF.parent.mkdir(parents=True,exist_ok=True);frames[0].save(OUT_GIF,save_all=True,append_images=frames[1:],duration=MS,loop=0,disposal=2,optimize=False)

def main():
    data=collect();OUT_JSON.parent.mkdir(parents=True,exist_ok=True);OUT_JSON.write_text(json.dumps(data,indent=2),encoding='utf-8');render(data);print(json.dumps(data,indent=2))
if __name__=='__main__':main()
