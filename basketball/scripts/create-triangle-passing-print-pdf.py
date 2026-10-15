#!/usr/bin/env python3
from importlib.util import module_from_spec,spec_from_file_location
from math import atan2,cos,pi,sin
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/"print"/"triangle-passing.pdf";PAGE_W,PAGE_H=letter;MARGIN=36
spec=spec_from_file_location("base",Path(__file__).with_name("create-close-out-drill-print-pdf.py"));base=module_from_spec(spec);spec.loader.exec_module(base)
STEPS=[
 {"title":"Form three lines","description":"Form two lines at the half-court corners and one under the basket. The front player under the basket starts with the ball.","positions":{"1a":(17,86),"2a":(50,25),"3a":(83,86),"1b":(17,95),"2b":(50,14),"3b":(83,95)},"ball":(50,25)},
 {"title":"Move to the ball","description":"The receiver steps toward the ball and catches. After passing, sprint to the end of the receiving line as that line advances.","positions":{"1a":(33.5,86),"2a":(17,95),"3a":(83,86),"1b":(17,86),"2b":(50,14),"3b":(83,95)},"ball":(33.5,86),"pass":((50,25),(33.5,86)),"move":((50,25),(17,95))},
 {"title":"Pass to the next line","description":"The next receiver moves to the ball. The passer delivers the pass, then sprints to the end of that receiving line.","positions":{"1a":(83,95),"2a":(17,95),"3a":(74.75,70.75),"1b":(17,86),"2b":(50,14),"3b":(83,86)},"ball":(72.25,67.25),"pass":((33.5,86),(74.75,70.75)),"move":((33.5,86),(83,95))},
 {"title":"Complete the triangle","description":"Continue the same pass-and-follow pattern to the third line, then repeat around the triangle with clear targets and communication.","positions":{"1a":(83,95),"2a":(17,95),"3a":(50,14),"1b":(17,86),"2b":(41.75,32),"3b":(83,86)},"ball":(41.75,32),"pass":((74.75,70.75),(41.75,32)),"move":((74.75,70.75),(50,14))},
]
def route(c,points,court,solid=False):
    pts=[base.pt(p,*court) for p in points];c.saveState();c.setStrokeColorRGB(.05,.05,.05);c.setLineWidth(1.2)
    if not solid:c.setDash(4,3)
    p=c.beginPath();p.moveTo(*pts[0]);p.lineTo(*pts[-1]);c.drawPath(p,stroke=1,fill=0);c.setDash();ex,ey=pts[-1];px,py=pts[-2];a=atan2(ey-py,ex-px);h=5.5;c.line(ex,ey,ex-h*cos(a-pi/6),ey-h*sin(a-pi/6));c.line(ex,ey,ex-h*cos(a+pi/6),ey-h*sin(a+pi/6));c.restoreState()
def ball(c,p):
    x,y=p;c.saveState();c.setFillColorRGB(1,1,1);c.setStrokeColorRGB(0,0,0);c.circle(x+5,y+5,3.3,fill=1,stroke=1);c.line(x+2,y+5,x+8,y+5);c.restoreState()
def step(c,n,s,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72);c.line(x,y,x+w,y);tx=x+16;c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",11);c.drawString(tx,y+h-22,f"STEP {n}");base.draw_text(c,s["title"].upper(),tx,y+h-41,210,size=10,leading=12,bold=True);base.draw_text(c,s["description"],tx,y+h-68,210,size=8.3,leading=10.2);court=(x+w-141,y+(h-102)/2,125,102);base.draw_half_court(c,*court)
    if s.get("move"):route(c,s["move"],court)
    if s.get("pass"):route(c,s["pass"],court,True)
    for label,pos in s["positions"].items():base.player(c,label,base.pt(pos,*court))
    ball(c,base.pt(s["ball"],*court))
def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1);c.setTitle("Triangle Passing - Decent.Coach Basket Ball Drills");c.setAuthor("Decent.Coach")
    c.setFillColorRGB(.96,.96,.96);c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0);c.drawImage(base.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto");c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",15);c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills");c.setFont("Helvetica",9);c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE");c.setFont("Helvetica-Bold",9);c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"TRIANGLE PASSING  |  1");c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23);c.drawString(MARGIN,PAGE_H-101,"Triangle Passing");c.setFont("Helvetica-Bold",9);c.drawString(MARGIN,PAGE_H-119,"PASSING  /  RECEIVING  /  COMMUNICATION");base.draw_text(c,"Three lines pass in sequence while receivers meet the ball and passers sprint to the end of the receiving line.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12);c.setStrokeColorRGB(.65,.65,.65);c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151);c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176);c.setFont("Helvetica-Bold",8);c.drawString(MARGIN+10,PAGE_H-167,"6+ PLAYERS   |   1 BALL   |   HALF COURT")
    for i,s in enumerate(STEPS):step(c,i+1,s,MARGIN,468-i*147,PAGE_W-2*MARGIN,147)
    c.setFont("Helvetica-Bold",7.5);c.drawString(MARGIN+16,43,"VARIATIONS");c.setFont("Helvetica",7.1);c.drawString(MARGIN+78,43,"Add a second ball, reverse direction, or change direction on command.");c.setFont("Helvetica",7);c.drawRightString(PAGE_W-MARGIN,16,"decent.coach");c.save();print(OUTPUT)
if __name__=="__main__":create_pdf()
