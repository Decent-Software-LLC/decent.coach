#!/usr/bin/env python3
from importlib.util import module_from_spec,spec_from_file_location
from math import atan2,cos,pi,sin
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/"print"/"horseshoe-shooting.pdf";PAGE_W,PAGE_H=letter;MARGIN=36
spec=spec_from_file_location("base",Path(__file__).with_name("create-close-out-drill-print-pdf.py"));base=module_from_spec(spec);spec.loader.exec_module(base)
STEPS=[
 {"title":"Set two baseline lines","description":"Form two lines on opposite sides of the key. Two balls begin in the lines, and the coach stands near the free-throw line.","positions":{"1":(28,72),"2":(72,72),"3":(28,82),"4":(72,82),"5":(28,91),"6":(72,91),"C":(50,49)},"balls":[(28,72),(72,82)]},
 {"title":"V-cut and receive","description":"The cutter changes direction sharply around the coach, calls for the ball, and presents a target for the pass.","positions":{"1":(28,72),"2":(40,39),"3":(28,82),"4":(72,82),"5":(28,91),"6":(72,91),"C":(50,49)},"balls":[(40,39),(72,82)],"move":((72,72),(50,34),(40,39)),"pass":((28,72),(40,39))},
 {"title":"Shoot and rebound","description":"Square to the basket, shoot with correct form, follow the shot, secure the rebound, and rotate to the opposite line.","positions":{"1":(28,72),"2":(72,91),"3":(28,82),"4":(72,72),"5":(28,91),"6":(72,82),"C":(50,49)},"balls":[(28,82),(72,72)],"move":((40,39),(50,25),(78,55),(72,91)),"pass":((40,39),(48,14),(50,25),(28,82))},
 {"title":"Rotate and continue","description":"Pass the rebound to the opposite line. The next cutter changes direction around the coach as the second ball keeps the drill moving.","positions":{"1":(60,39),"2":(72,91),"3":(28,72),"4":(72,72),"5":(28,82),"6":(72,82),"C":(50,49)},"balls":[(28,72),(60,39)],"move":((28,72),(50,34),(60,39)),"pass":((72,72),(60,39))},
]
def route(c,points,court,solid=False):
    pts=[base.pt(p,*court) for p in points];c.saveState();c.setStrokeColorRGB(.05,.05,.05);c.setLineWidth(1.2)
    if not solid:c.setDash(4,3)
    p=c.beginPath();p.moveTo(*pts[0]);[p.lineTo(*q) for q in pts[1:]];c.drawPath(p,stroke=1,fill=0);c.setDash();ex,ey=pts[-1];px,py=pts[-2];a=atan2(ey-py,ex-px);h=5.5;c.line(ex,ey,ex-h*cos(a-pi/6),ey-h*sin(a-pi/6));c.line(ex,ey,ex-h*cos(a+pi/6),ey-h*sin(a+pi/6));c.restoreState()
def ball(c,p):
    x,y=p;c.saveState();c.setFillColorRGB(1,1,1);c.setStrokeColorRGB(0,0,0);c.circle(x+5,y+5,3.3,fill=1,stroke=1);c.line(x+2,y+5,x+8,y+5);c.restoreState()
def step(c,n,s,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72);c.line(x,y,x+w,y);tx=x+16;c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",11);c.drawString(tx,y+h-22,f"STEP {n}");base.draw_text(c,s["title"].upper(),tx,y+h-41,210,size=10,leading=12,bold=True);base.draw_text(c,s["description"],tx,y+h-68,210,size=8.3,leading=10.2);court=(x+w-141,y+(h-102)/2,125,102);base.draw_half_court(c,*court)
    if s.get("move"):route(c,s["move"],court)
    if s.get("pass"):route(c,s["pass"],court,True)
    for label,pos in s["positions"].items():base.player(c,label,base.pt(pos,*court),defense=label=="C")
    for pos in s["balls"]:ball(c,base.pt(pos,*court))
def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1);c.setTitle("Horseshoe Shooting - Decent.Coach Basket Ball Drills");c.setAuthor("Decent.Coach");
    c.setFillColorRGB(.96,.96,.96);c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0);c.drawImage(base.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto");c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",15);c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills");c.setFont("Helvetica",9);c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE");c.setFont("Helvetica-Bold",9);c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"HORSESHOE SHOOTING  |  1");c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23);c.drawString(MARGIN,PAGE_H-101,"Horseshoe Shooting");c.setFont("Helvetica-Bold",9);c.drawString(MARGIN,PAGE_H-119,"SHOOTING  /  PASSING  /  RECEIVING");base.draw_text(c,"Two baseline lines alternate hard cuts, catches, shots, rebounds, and rotations through the opposite line.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12);c.setStrokeColorRGB(.65,.65,.65);c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151);c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176);c.setFont("Helvetica-Bold",8);c.drawString(MARGIN+10,PAGE_H-167,"ALL PLAYERS   |   2 BALLS   |   HALF COURT")
    for i,s in enumerate(STEPS):step(c,i+1,s,MARGIN,468-i*147,PAGE_W-2*MARGIN,147)
    c.setFont("Helvetica-Bold",7.5);c.drawString(MARGIN+16,43,"VARIATIONS");c.setFont("Helvetica",7.1);c.drawString(MARGIN+78,43,"Shoot off one dribble, drive to the basket, or add a shot fake.");c.setFont("Helvetica",7);c.drawRightString(PAGE_W-MARGIN,16,"decent.coach");c.save();print(OUTPUT)
if __name__=="__main__":create_pdf()
