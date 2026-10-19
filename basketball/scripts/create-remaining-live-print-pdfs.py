#!/usr/bin/env python3
import json
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from math import atan2, cos, pi, sin
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]; PAGE_W,PAGE_H=letter; MARGIN=36
SLUGS=["five-corner-passing","five-on-four-plus-one","full-court-four-line-passing","lay-up-and-rebounding-lines","ten-fingers"]
spec=spec_from_file_location("half",Path(__file__).with_name("create-close-out-drill-print-pdf.py"));half=module_from_spec(spec);spec.loader.exec_module(half)
spec=spec_from_file_location("full",Path(__file__).with_name("create-line-running-drills-print-pdf.py"));full=module_from_spec(spec);spec.loader.exec_module(full)


def load_drills():
    script="""global.window={BASKETBALL_DRILLS:{}};const fs=%s;for(const f of fs)require('./data/drills/'+f+'.js');console.log(JSON.stringify(fs.map(f=>window.BASKETBALL_DRILLS[f])));"""%json.dumps(SLUGS)
    result=subprocess.run(["node","-e",script],cwd=ROOT,text=True,capture_output=True,check=True)
    drills=json.loads(result.stdout)
    for drill in drills:
        if drill["id"]=="five-on-four-plus-one":
            drill["steps"][1]["description"]="After the coach passes to an offensive player, the defender across from the receiver runs to the baseline and waits for the coach's release before joining the defenders."
        if drill["id"]=="full-court-four-line-passing":
            second_ball_players=("p2","p4","p1","p4","p4")
            for step,pid in zip(drill["steps"],second_ball_players):
                step["extraBalls"]={"second":{"position":step["positions"][pid]}}
    return drills


def pt(position,court): return half.pt(position,*court)


def route(c,points,court,solid=False):
    points=[p.get("position",p) if isinstance(p,dict) else p for p in points]
    if len(points)<2:return
    mapped=[pt(p,court) for p in points]; sx,sy=mapped[0];nx,ny=mapped[1];dx,dy=nx-sx,ny-sy;length=max((dx*dx+dy*dy)**.5,1);mapped[0]=(sx+dx/length*7,sy+dy/length*7)
    px,py=mapped[-2];ex,ey=mapped[-1];dx,dy=ex-px,ey-py;length=max((dx*dx+dy*dy)**.5,1);mapped[-1]=(ex-dx/length*7,ey-dy/length*7)
    c.saveState();c.setStrokeColorRGB(.04,.04,.04);c.setLineWidth(1.1)
    if not solid:c.setDash(4,3)
    p=c.beginPath();p.moveTo(*mapped[0])
    for point in mapped[1:]:p.lineTo(*point)
    c.drawPath(p,stroke=1,fill=0);c.setDash();ex,ey=mapped[-1];px,py=mapped[-2];a=atan2(ey-py,ex-px);h=5
    c.line(ex,ey,ex-h*cos(a-pi/6),ey-h*sin(a-pi/6));c.line(ex,ey,ex-h*cos(a+pi/6),ey-h*sin(a+pi/6));c.restoreState()


def player(c,label,point,team):
    x,y=point;c.saveState();c.setStrokeColorRGB(0,0,0);c.setLineWidth(1)
    if team in ("defense","neutral"):c.setFillColorRGB(1,1,1);c.circle(x,y,6.5,fill=1,stroke=1);c.setFillColorRGB(0,0,0)
    else:c.setFillColorRGB(.08,.08,.08);c.circle(x,y,6.5,fill=1,stroke=1);c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold",5.5 if len(label)>1 else 7);c.drawCentredString(x,y-2,label);c.restoreState()


def ball(c,point):
    x,y=point;c.saveState();c.setFillColorRGB(1,1,1);c.setStrokeColorRGB(0,0,0);c.setLineWidth(.7);c.circle(x+5,y+5,3.1,fill=1,stroke=1);c.line(x+2,y+5,x+8,y+5);c.restoreState()


def draw_step(c,n,step,prev,players,court_type,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72);c.setLineWidth(.7);c.line(x,y,x+w,y);tx=x+16;c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",10.5);c.drawString(tx,y+h-18,f"STEP {n}")
    half.draw_text(c,step["title"].upper(),tx,y+h-35,210,size=9.2,leading=10.5,bold=True);half.draw_text(c,step["description"],tx,y+h-56,210,size=7.7,leading=9.1)
    if court_type=="full":court=(x+w-182,y+(h-88)/2,166,88);full.draw_full_court(c,*court)
    else:court=(x+w-127,y+(h-92)/2,111,92);half.draw_half_court(c,*court)
    movements=step.get("movements") or []
    moved=set()
    for movement in movements:
        pid=movement.get("player");points=[p.get("position") for p in movement.get("points",[]) if p.get("position")]
        if len(points)>1:route(c,points,court);moved.add(pid)
    if prev:
        for pid,end in step["positions"].items():
            start=prev["positions"].get(pid)
            if start and start!=end and pid not in moved:route(c,[start,end],court)
    if step.get("ballPath"):route(c,step["ballPath"],court,True)
    for extra in (step.get("extraBalls") or {}).values():
        if extra.get("path"):route(c,extra["path"],court,True)
    for pid,pos in step["positions"].items():
        info=players.get(pid,{"label":pid,"team":"offense"});player(c,info["label"],pt(pos,court),info.get("team","offense"))
    ball_pos=step.get("ballPosition")
    if not ball_pos and step.get("ball") in step["positions"]:ball_pos=step["positions"][step["ball"]]
    if ball_pos:ball(c,pt(ball_pos,court))
    for extra in (step.get("extraBalls") or {}).values():
        if extra.get("position"):ball(c,pt(extra["position"],court))


def create_pdf(drill):
    slug=drill["id"];output=ROOT/"print"/f"{slug}.pdf";output.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(output),pagesize=letter,pageCompression=1);c.setTitle(f'{drill["title"]} - Decent.Coach Basket Ball Drills');c.setAuthor("Decent.Coach")
    c.setFillColorRGB(.96,.96,.96);c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0);c.drawImage(half.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto");c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",15);c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills");c.setFont("Helvetica",9);c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE");c.setFont("Helvetica-Bold",8.5);c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,f'{drill["title"].upper()}  |  1');c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",22);c.drawString(MARGIN,PAGE_H-101,drill["title"]);categories="  /  ".join(drill.get("categories",[])[:3]).upper();c.setFont("Helvetica-Bold",8.5);c.drawString(MARGIN,PAGE_H-119,categories);half.draw_text(c,drill.get("summary",""),MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=8.8,leading=11)
    c.setStrokeColorRGB(.65,.65,.65);c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151);c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176);eq=drill.get("equipment",{});players=eq.get("playersLabel") or str(eq.get("players","ALL PLAYERS"));balls=eq.get("basketballs",0);ball_label="BALL" if balls==1 else "BALLS";court_label=drill.get("court",{}).get("label","COURT");c.setFont("Helvetica-Bold",8);c.drawString(MARGIN+10,PAGE_H-167,f'{str(players).upper()}   |   {balls} {ball_label}   |   {court_label.upper()}')
    steps=drill["steps"];row_h=112 if len(steps)>=5 else 140;base_y=48;players_by_id={p["id"]:p for p in drill["players"]}
    for i,step in enumerate(steps):draw_step(c,i+1,step,steps[i-1] if i else None,players_by_id,drill["court"]["type"],MARGIN,base_y+(len(steps)-1-i)*row_h,PAGE_W-2*MARGIN,row_h)
    variations=drill.get("variations") or []
    if variations:c.setFont("Helvetica-Bold",7.2);c.drawString(MARGIN+16,31,"VARIATION");c.setFont("Helvetica",6.8);half.draw_text(c,variations[0],MARGIN+72,31,PAGE_W-MARGIN-(MARGIN+72),size=6.8,leading=8)
    c.setFont("Helvetica",7);c.drawRightString(PAGE_W-MARGIN,16,"decent.coach");c.save();print(output)


if __name__=="__main__":
    requested=set(sys.argv[1:])
    for drill in load_drills():
        if not requested or drill["id"] in requested:create_pdf(drill)
