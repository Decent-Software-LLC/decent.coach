#!/usr/bin/env python3
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]; OUTPUT=ROOT/"print"/"knockout.pdf"; PAGE_W,PAGE_H=letter; MARGIN=36
spec=spec_from_file_location("base",Path(__file__).with_name("create-close-out-drill-print-pdf.py")); base=module_from_spec(spec); spec.loader.exec_module(base)
STEPS=[
 {"title":"Form one shooting line","description":"Line up at the free-throw line. The first two players begin with basketballs.","positions":{"p1":(50,49),"p2":(50,58),"p3":(50,67),"p4":(50,76),"p5":(50,85)},"balls":[(50,49),(50,58)]},
 {"title":"First shooter releases","description":"The lead player shoots with correct form and waits until the ball reaches the rim before pursuing it.","positions":{"p1":(50,41),"p2":(50,58),"p3":(50,67),"p4":(50,76),"p5":(50,85)},"balls":[(50,20),(50,58)],"paths":[((50,49),(50,12),(50,20))]},
 {"title":"Second shooter gives chase","description":"The next player shoots. The lead player rebounds and keeps shooting after a miss while the trailing shooter races to score first.","positions":{"p1":(43,28),"p2":(50,41),"p3":(50,58),"p4":(50,67),"p5":(50,76)},"balls":[(43,28),(50,20)],"paths":[((50,41),(43,28)),((50,58),(50,12),(50,20))]},
 {"title":"Score, return, and rotate","description":"After scoring, rebound and return the ball to the next player, then join the end of the line. A trailing score knocks out the player ahead.","positions":{"p1":(50,85),"p2":(50,32),"p3":(50,49),"p4":(50,58),"p5":(50,67)},"balls":[(50,49),(50,32)],"paths":[((43,28),(30,48),(35,78),(50,85)),((43,28),(50,49))]},
]
def path(c,points,court):
    mapped=[base.pt(p,*court) for p in points]
    for a,b in zip(mapped,mapped[1:]): base.arrow(c,[a,b])
def ball(c,p):
    x,y=p;c.saveState();c.setFillColorRGB(1,1,1);c.setStrokeColorRGB(0,0,0);c.circle(x+5,y+5,3.4,fill=1,stroke=1);c.line(x+2,y+5,x+8,y+5);c.restoreState()
def draw_step(c,n,s,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72);c.line(x,y,x+w,y);tx=x+16;c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",11);c.drawString(tx,y+h-22,f"STEP {n}");base.draw_text(c,s["title"].upper(),tx,y+h-41,210,size=10,leading=12,bold=True);base.draw_text(c,s["description"],tx,y+h-68,210,size=8.3,leading=10.2)
    court=(x+w-141,y+(h-102)/2,125,102);base.draw_half_court(c,*court)
    for p in s.get("paths",[]):path(c,p,court)
    for pid,pos in s["positions"].items():base.player(c,pid[-1],base.pt(pos,*court))
    for pos in s["balls"]:ball(c,base.pt(pos,*court))
def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True);c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1);c.setTitle("Knockout - Decent.Coach Basket Ball Drills");c.setAuthor("Decent.Coach")
    c.setFillColorRGB(.96,.96,.96);c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0);c.drawImage(base.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto");c.setFillColorRGB(0,0,0);c.setFont("Helvetica-Bold",15);c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills");c.setFont("Helvetica",9);c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE");c.setFont("Helvetica-Bold",9);c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"KNOCKOUT  |  1");c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23);c.drawString(MARGIN,PAGE_H-101,"Knockout");c.setFont("Helvetica-Bold",9);c.drawString(MARGIN,PAGE_H-119,"SHOOTING  /  REBOUNDING  /  COMPETITION");base.draw_text(c,"Two shooters race to score, rebound, and return the ball before the trailing shooter makes a basket.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12);c.setStrokeColorRGB(.65,.65,.65);c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151);c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176);c.setFont("Helvetica-Bold",8);c.drawString(MARGIN+10,PAGE_H-167,"ALL PLAYERS   |   2 BALLS   |   HALF COURT")
    for i,s in enumerate(STEPS):draw_step(c,i+1,s,MARGIN,468-i*147,PAGE_W-2*MARGIN,147)
    c.setFont("Helvetica-Bold",7.5);c.drawString(MARGIN+16,43,"VARIATION");c.setFont("Helvetica",7.5);c.drawString(MARGIN+72,43,"Start the first shot from the wing or three-point line.");c.setFont("Helvetica",7);c.drawRightString(PAGE_W-MARGIN,16,"decent.coach");c.save();print(OUTPUT)
if __name__=="__main__":create_pdf()
