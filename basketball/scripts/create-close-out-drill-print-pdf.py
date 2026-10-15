#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"print"/"close-out-drill.pdf"
LOGO=ROOT/"assets"/"branding"/"decent-basketball.png"
PAGE_W,PAGE_H=letter
MARGIN=36

OFFENSE={"o1":(83,35),"o2":(66,68),"o3":(34,68),"o4":(17,35)}
STEPS=[
    {"title":"Set the four spots","description":"Four offensive players begin in triple-threat stance around the arc. The remaining players form the defensive line. No ball is used.","positions":{**OFFENSE,"d1":(50,17),"d2":(46,2),"d3":(50,2),"d4":(54,2)}},
    {"title":"Close out the first player","description":"The first defender closes out using a bunny hop or stutter step, calls 'ball,' and finishes under control in a defensive stance.","positions":{**OFFENSE,"d1":(78,35),"d2":(50,17),"d3":(50,2),"d4":(54,2)},"moves":{"d1":((50,17),(78,35)),"d2":((46,2),(50,17))}},
    {"title":"Recover to the next player","description":"React to a one-step offensive move with a drop step and quick slide, then recover as the next defender begins the closeout.","positions":{**OFFENSE,"d1":(59,60),"d2":(78,35),"d3":(50,17),"d4":(54,2)},"moves":{"d1":((78,35),(58,35),(59,60)),"d2":((50,17),(78,35)),"d3":((50,2),(50,17))}},
    {"title":"Rotate through three closeouts","description":"Continue the closeout, drop-step, quick-slide, and recovery sequence while maintaining stance and communication.","positions":{**OFFENSE,"d1":(41,60),"d2":(59,60),"d3":(78,35),"d4":(50,17)},"moves":{"d1":((59,60),(50,35),(41,60)),"d2":((78,35),(58,35),(59,60)),"d3":((50,17),(78,35)),"d4":((54,2),(50,17))}},
    {"title":"Continue rotations and rotate players","description":"Complete the sequence, then rotate personnel. The lead defender joins offense, each offensive player advances, and the final player joins the defensive line."},
]


def gray_logo():
    source=Image.open(LOGO).convert("RGBA"); alpha=source.getchannel("A"); gray=ImageEnhance.Contrast(ImageOps.grayscale(source.convert("RGB"))).enhance(1.45)
    return ImageReader(Image.merge("RGBA",(gray,gray,gray,alpha)))


def wrap_lines(text,font,size,width):
    lines,current=[],""
    for word in text.split():
        trial=f"{current} {word}".strip()
        if stringWidth(trial,font,size)<=width: current=trial
        else:
            if current: lines.append(current)
            current=word
    if current: lines.append(current)
    return lines


def draw_text(c,text,x,y,width,size=9,leading=11,bold=False):
    font="Helvetica-Bold" if bold else "Helvetica"; c.setFont(font,size)
    for line in wrap_lines(text,font,size,width): c.drawString(x,y,line); y-=leading
    return y


def pt(position,x,y,w,h): return x+position[0]/100*w,y+(1-position[1]/100)*h


def draw_half_court(c,x,y,w,h):
    c.saveState(); c.setFillColorRGB(1,1,1); c.setStrokeColorRGB(.08,.08,.08); c.setLineWidth(1); c.rect(x,y,w,h,fill=1,stroke=1)
    lane_w,lane_h=w*.29,h*.38; lane_x=x+(w-lane_w)/2; lane_y=y+h-lane_h
    c.rect(lane_x,lane_y,lane_w,lane_h,fill=0,stroke=1); c.circle(x+w/2,lane_y,lane_w/2,fill=0,stroke=1)
    c.setDash(3,3); c.arc(x+w/2-lane_w/2,lane_y-lane_w/2,x+w/2+lane_w/2,lane_y+lane_w/2,0,180); c.setDash()
    hoop_y=y+h-h*.115; c.setLineWidth(2); c.line(x+w*.42,hoop_y+h*.025,x+w*.58,hoop_y+h*.025); c.setLineWidth(1); c.circle(x+w/2,hoop_y,w*.022,fill=0,stroke=1)
    c.line(x+w*.09,y+h,x+w*.09,y+h*.80); c.line(x+w*.91,y+h,x+w*.91,y+h*.80)
    arc=c.beginPath(); arc.moveTo(x+w*.09,y+h*.80); arc.curveTo(x+w*.14,y+h*.46,x+w*.34,y+h*.34,x+w*.50,y+h*.34); arc.curveTo(x+w*.66,y+h*.34,x+w*.86,y+h*.46,x+w*.91,y+h*.80); c.drawPath(arc,stroke=1,fill=0); c.restoreState()


def arrow(c,points):
    points=list(points); sx,sy=points[0]; ex,ey=points[-1]
    first_dx,first_dy=points[1][0]-sx,points[1][1]-sy; first_len=max((first_dx*first_dx+first_dy*first_dy)**.5,1); points[0]=(sx+first_dx/first_len*8,sy+first_dy/first_len*8)
    last_dx,last_dy=ex-points[-2][0],ey-points[-2][1]; last_len=max((last_dx*last_dx+last_dy*last_dy)**.5,1); points[-1]=(ex-last_dx/last_len*8,ey-last_dy/last_len*8)
    c.saveState(); c.setStrokeColorRGB(.05,.05,.05); c.setLineWidth(1.15); c.setDash(4,3)
    path=c.beginPath(); path.moveTo(*points[0])
    for point in points[1:]: path.lineTo(*point)
    c.drawPath(path,stroke=1,fill=0); c.setDash(); ex,ey=points[-1]; angle=atan2(ey-points[-2][1],ex-points[-2][0]); head=5.5
    c.line(ex,ey,ex-head*cos(angle-pi/6),ey-head*sin(angle-pi/6)); c.line(ex,ey,ex-head*cos(angle+pi/6),ey-head*sin(angle+pi/6)); c.restoreState()


def player(c,label,point,defense=False):
    x,y=point; c.saveState(); c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.2)
    if defense: c.setFillColorRGB(1,1,1); c.circle(x,y,7,fill=1,stroke=1); c.setFillColorRGB(0,0,0)
    else: c.setFillColorRGB(.08,.08,.08); c.circle(x,y,7,fill=1,stroke=1); c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold",6.5 if len(label)>1 else 7.5); c.drawCentredString(x,y-2.4,label); c.restoreState()


def draw_step(c,number,step,x,y,w,h,show_diagram=True):
    c.setStrokeColorRGB(.72,.72,.72); c.setLineWidth(.7); c.line(x,y,x+w,y); tx,tw=x+16,205; c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",11); c.drawString(tx,y+h-20,f"STEP {number}")
    draw_text(c,step["title"].upper(),tx,y+h-38,tw,size=10,leading=12,bold=True); draw_text(c,step["description"],tx,y+h-62,tw,size=8.2,leading=10.2)
    if not show_diagram:
        vx,vy=x+300,y+h-20; c.setFont("Helvetica-Bold",9); c.drawString(vx,vy,"VARIATION"); vy-=14; c.setFont("Helvetica-Bold",7); c.drawString(vx,vy,"-"); draw_text(c,"Practice both bunny-hop and stutter-step closeout methods.",vx+9,vy,x+w-vx-9,size=7.2,leading=8.8); return
    court_w=125; court_h=court_w/(1090.86/912.61); court_x=x+w-16-court_w; court_y=y+(h-court_h)/2; draw_half_court(c,court_x,court_y,court_w,court_h)
    for motion in step.get("moves",{}).values(): arrow(c,[pt(position,court_x,court_y,court_w,court_h) for position in motion])
    for pid,pos in step["positions"].items(): player(c,pid[-1] if pid.startswith("o") else f"X{pid[-1]}",pt(pos,court_x,court_y,court_w,court_h),defense=pid.startswith("d"))


def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1); c.setTitle("Close Out Drill - Decent.Coach Basket Ball Drills"); c.setAuthor("Decent.Coach"); c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96,.96,.96); c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0); c.drawImage(gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto"); c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",15); c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills"); c.setFont("Helvetica",9); c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE"); c.setFont("Helvetica-Bold",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"CLOSE OUT DRILL  |  1"); c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23); c.drawString(MARGIN,PAGE_H-101,"Close Out Drill"); c.setFont("Helvetica-Bold",9); c.drawString(MARGIN,PAGE_H-119,"DEFENSE  /  FOOTWORK  /  RECOVERY"); c.setFont("Helvetica",9); draw_text(c,"Defenders close out four perimeter players, react to a jab step, and recover before rotating assignments.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12)
    c.setStrokeColorRGB(.65,.65,.65); c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151); c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176); c.setFont("Helvetica-Bold",8); c.drawString(MARGIN+10,PAGE_H-167,"8 PLAYERS   |   0 BALLS   |   HALF COURT")
    draw_step(c,1,STEPS[0],MARGIN,500,PAGE_W-2*MARGIN,115); draw_step(c,2,STEPS[1],MARGIN,385,PAGE_W-2*MARGIN,115); draw_step(c,3,STEPS[2],MARGIN,270,PAGE_W-2*MARGIN,115); draw_step(c,4,STEPS[3],MARGIN,155,PAGE_W-2*MARGIN,115); draw_step(c,5,STEPS[4],MARGIN,40,PAGE_W-2*MARGIN,115,show_diagram=False)
    c.setFont("Helvetica",7); c.drawRightString(PAGE_W-MARGIN,16,"decent.coach"); c.save(); print(OUTPUT)


if __name__=="__main__": create_pdf()
