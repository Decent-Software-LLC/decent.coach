#!/usr/bin/env python3
from importlib.util import module_from_spec, spec_from_file_location
from math import atan2, cos, pi, sin
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/"print"/"three-player-weave.pdf";PAGE_W,PAGE_H=letter;MARGIN=36
spec=spec_from_file_location("base",Path(__file__).with_name("create-line-running-drills-print-pdf.py"));base=module_from_spec(spec);spec.loader.exec_module(base)
STEPS=[
 {"title":"Start in three lanes","description":"Form three baseline lanes. The middle player begins with the ball.","positions":{"1":(5,50),"2":(5,29),"3":(5,71)},"ball":(5,50),"paths":{"1":((5,50),(15,50),(24,38),(32,29)),"2":((5,29),(15,29),(21,40),(27,50)),"3":((5,71),(27,71)),"ball":((5,50),(15,29),(21,40),(27,50))}},
 {"title":"Pass, then exchange lanes","description":"All three advance. The middle player passes outside and cuts in front of the receiver; the receiver carries the ball into the middle lane.","positions":{"1":(32,29),"2":(27,50),"3":(27,71)},"ball":(27,50),"paths":{"1":((32,29),(52,29)),"2":((27,50),(40,50),(48,62),(56,71)),"3":((27,71),(40,71),(46,61),(51,50)),"ball":((27,50),(40,71),(46,61),(51,50))}},
 {"title":"Pass and exchange again","description":"Pass to the opposite outside lane. The passer cuts in front of the receiver while the receiver brings the ball into the middle.","positions":{"1":(52,29),"2":(56,71),"3":(51,50)},"ball":(51,50),"paths":{"1":((52,29),(64,29),(73,39),(84,50)),"2":((56,71),(82,66)),"3":((51,50),(64,50),(76,41),(88,34)),"ball":((51,50),(64,29),(73,39),(84,50))}},
 {"title":"Finish at the rim","description":"Make the final pass ahead. The passer cuts in front of the receiver, who enters the middle lane and attacks the basket while the third player fills outside.","positions":{"1":(84,50),"2":(82,66),"3":(88,34)},"ball":(84,50)},
]
def path(c,points,court,solid=False):
    mapped=[base.pt(p,*court) for p in points]
    sx,sy=mapped[0]; nx,ny=mapped[1]; dx,dy=nx-sx,ny-sy; length=max((dx*dx+dy*dy)**.5,1); mapped[0]=(sx+dx/length*8,sy+dy/length*8)
    px,py=mapped[-2]; ex,ey=mapped[-1]; dx,dy=ex-px,ey-py; length=max((dx*dx+dy*dy)**.5,1); mapped[-1]=(ex-dx/length*8,ey-dy/length*8)
    c.saveState();c.setStrokeColorRGB(.05,.05,.05);c.setLineWidth(1.25)
    if not solid:c.setDash(4,3)
    route=c.beginPath();route.moveTo(*mapped[0])
    for point in mapped[1:]:route.lineTo(*point)
    c.drawPath(route,stroke=1,fill=0);c.setDash();ex,ey=mapped[-1];px,py=mapped[-2];angle=atan2(ey-py,ex-px);head=5.5
    c.line(ex,ey,ex-head*cos(angle-pi/6),ey-head*sin(angle-pi/6));c.line(ex,ey,ex-head*cos(angle+pi/6),ey-head*sin(angle+pi/6));c.restoreState()
def ball(c,p):
    x,y=p;c.saveState();c.setFillColorRGB(1,1,1);c.setStrokeColorRGB(0,0,0);c.circle(x+5,y+5,3.4,fill=1,stroke=1);c.line(x+2,y+5,x+8,y+5);c.restoreState()
def draw_step(c,n,s,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72);c.line(x,y,x+w,y);tx=x+16;c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",11);c.drawString(tx,y+h-22,f"STEP {n}");base.draw_text(c,s["title"].upper(),tx,y+h-41,210,size=10,leading=12,bold=True);base.draw_text(c,s["description"],tx,y+h-68,210,size=8.3,leading=10.2)
    court=(x+w-182,y+(h-100)/2,166,100);base.draw_full_court(c,*court)
    for key,p in s.get("paths",{}).items():path(c,p,court,solid=key=="ball")
    for pid,pos in s["positions"].items():base.player(c,pid,base.pt(pos,*court))
    ball(c,base.pt(s["ball"],*court))
def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1);c.setTitle("Three-Player Weave - Decent.Coach Basket Ball Drills");c.setAuthor("Decent.Coach")
    c.setFillColorRGB(.96,.96,.96);c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0);c.drawImage(base.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto");c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",15);c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills");c.setFont("Helvetica",9);c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE");c.setFont("Helvetica-Bold",9);c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"THREE-PLAYER WEAVE  |  1");c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23);c.drawString(MARGIN,PAGE_H-101,"Three-Player Weave");c.setFont("Helvetica-Bold",9);c.drawString(MARGIN,PAGE_H-119,"PASSING  /  TRANSITION  /  LANE SPACING");base.draw_text(c,"Three players pass ahead and exchange lanes, with each receiver carrying the ball into the middle lane.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12);c.setStrokeColorRGB(.65,.65,.65);c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151);c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176);c.setFont("Helvetica-Bold",8);c.drawString(MARGIN+10,PAGE_H-167,"3 PLAYERS   |   1 BALL   |   FULL COURT")
    for i,s in enumerate(STEPS):draw_step(c,i+1,s,MARGIN,468-i*147,PAGE_W-2*MARGIN,147)
    c.setFont("Helvetica-Bold",7.5);c.drawString(MARGIN+16,43,"VARIATIONS");c.setFont("Helvetica",7.2);c.drawString(MARGIN+78,43,"Return in the opposite direction, or specify the pass type for each trip.");c.setFont("Helvetica",7);c.drawRightString(PAGE_W-MARGIN,16,"decent.coach");c.save();print(OUTPUT)
if __name__=="__main__":create_pdf()
