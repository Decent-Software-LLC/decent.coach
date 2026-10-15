#!/usr/bin/env python3
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("print_base", Path(__file__).with_name("create-line-running-drills-print-pdf.py"))
base = module_from_spec(spec)
spec.loader.exec_module(base)

OUTPUT = ROOT / "print" / "line-dribbling-drills.pdf"
PAGE_W, PAGE_H = letter
MARGIN = 36
STEPS = [
    {"title":"Set four dribbling lanes","description":"Form four baseline lines. Each player begins low and balanced with a basketball, fingertips active and eyes up.","positions":{"p1":(7,20),"p2":(7,40),"p3":(7,60),"p4":(7,80)}},
    {"title":"Change pace under control","description":"Use a speed dribble, then lower the body and shift into a protected control dribble at the designated mark.","positions":{"p1":(31,20),"p2":(31,40),"p3":(31,60),"p4":(31,80)},"moves":{"p1":((7,20),(31,20)),"p2":((7,40),(31,40)),"p3":((7,60),(31,60)),"p4":((7,80),(31,80))}},
    {"title":"Execute the designated move","description":"At the next mark, use the selected crossover, inside-out, reverse, or hesitation move while protecting the ball.","positions":{"p1":(54,27),"p2":(54,34),"p3":(54,67),"p4":(54,73)},"moves":{"p1":((31,20),(43,20),(54,27)),"p2":((31,40),(43,40),(54,34)),"p3":((31,60),(43,60),(54,67)),"p4":((31,80),(43,80),(54,73))}},
    {"title":"Attack out of the move","description":"Plant the outside foot, push off explosively, and accelerate into open court without losing balance or looking down.","positions":{"p1":(78,27),"p2":(78,34),"p3":(78,67),"p4":(78,73)},"moves":{"p1":((54,27),(78,27)),"p2":((54,34),(78,34)),"p3":((54,67),(78,67)),"p4":((54,73),(78,73))}},
    {"title":"Finish and change direction","description":"Finish under control at the far end. On the next repetition, use a zig-zag route with additional changes of hand and direction.","positions":{"p1":(92,35),"p2":(92,44),"p3":(92,56),"p4":(92,65)},"moves":{"p1":((78,27),(85,27),(92,35)),"p2":((78,34),(85,34),(92,44)),"p3":((78,67),(85,67),(92,56)),"p4":((78,73),(85,73),(92,65))}},
]


def path_arrow(c, points, court):
    mapped = [base.pt(point, *court) for point in points]
    for start, end in zip(mapped, mapped[1:]):
        base.arrow(c, start, end)


def ball(c, point):
    x, y = point
    c.saveState(); c.setFillColorRGB(1,1,1); c.setStrokeColorRGB(0,0,0); c.setLineWidth(.8)
    c.circle(x+5.5,y+5.5,3.2,fill=1,stroke=1); c.line(x+2.5,y+5.5,x+8.5,y+5.5); c.restoreState()


def draw_step(c, number, step, x, y, w, h):
    c.setStrokeColorRGB(.72,.72,.72); c.setLineWidth(.7); c.line(x,y,x+w,y)
    tx,tw=x+16,210; c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",11); c.drawString(tx,y+h-19,f"STEP {number}")
    base.draw_text(c,step["title"].upper(),tx,y+h-37,tw,size=9.5,leading=11,bold=True)
    base.draw_text(c,step["description"],tx,y+h-60,tw,size=8.1,leading=9.8)
    court=(x+w-182,y+(h-90)/2,166,90); base.draw_full_court(c,*court)
    for motion in step.get("moves",{}).values(): path_arrow(c,motion,court)
    for pid,position in step["positions"].items():
        point=base.pt(position,*court); base.player(c,pid[-1],point); ball(c,point)


def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1); c.setTitle("Line Dribbling Drills - Decent.Coach Basket Ball Drills"); c.setAuthor("Decent.Coach"); c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96,.96,.96); c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0); c.drawImage(base.gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto")
    c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",15); c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills"); c.setFont("Helvetica",9); c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE"); c.setFont("Helvetica-Bold",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"LINE DRIBBLING DRILLS  |  1"); c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23); c.drawString(MARGIN,PAGE_H-101,"Line Dribbling Drills"); c.setFont("Helvetica-Bold",9); c.drawString(MARGIN,PAGE_H-119,"DRIBBLING  /  BALL HANDLING  /  CHANGE OF PACE")
    base.draw_text(c,"Players advance in lanes while controlling pace, direction, and hand changes at designated court marks.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12)
    c.setStrokeColorRGB(.65,.65,.65); c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151); c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176); c.setFont("Helvetica-Bold",8); c.drawString(MARGIN+10,PAGE_H-167,"ALL PLAYERS   |   1 BALL EACH   |   FULL COURT")
    heights=115
    for index,step in enumerate(STEPS): draw_step(c,index+1,step,MARGIN,500-index*heights,PAGE_W-2*MARGIN,heights)
    c.setFont("Helvetica-Bold",7.4); c.drawString(MARGIN+16,44,"VARIATION"); c.setFont("Helvetica",7.2); c.drawString(MARGIN+72,44,"Use follow-the-leader, with every player copying the designated leader's moves.")
    c.setFont("Helvetica",7); c.drawRightString(PAGE_W-MARGIN,16,"decent.coach"); c.save(); print(OUTPUT)


if __name__=="__main__": create_pdf()
