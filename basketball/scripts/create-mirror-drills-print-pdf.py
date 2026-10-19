#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"print"/"mirror-drills.pdf"
LOGO=ROOT/"assets"/"branding"/"decent-basketball.png"
PAGE_W,PAGE_H=letter
MARGIN=36

STEPS=[
    {"title":"Set a defensive stance","description":"Form a straight line facing the coach. Begin low and balanced with feet wide, chest up, and hands active.","positions":{"d1":(50,28),"d2":(50,38),"d3":(50,48),"d4":(50,58),"d5":(50,68),"c":(50,82)}},
    {"title":"Mirror the coach","description":"Slide with the coach while staying in line, maintaining spacing, and keeping the feet from crossing.","positions":{"d1":(31,28),"d2":(31,38),"d3":(31,48),"d4":(31,58),"d5":(31,68),"c":(31,82)},"moves":{"d1":((50,28),(31,28)),"d2":((50,38),(31,38)),"d3":((50,48),(31,48)),"d4":((50,58),(31,58)),"d5":((50,68),(31,68)),"c":((50,82),(31,82))}},
    {"title":"Change direction quickly","description":"After no more than three steps, push off the outside foot, change direction, and stay square without crossing the feet.","positions":{"d1":(69,28),"d2":(69,38),"d3":(69,48),"d4":(69,58),"d5":(69,68),"c":(69,82)},"moves":{"d1":((31,28),(69,28)),"d2":((31,38),(69,38)),"d3":((31,48),(69,48)),"d4":((31,58),(69,58)),"d5":((31,68),(69,68)),"c":((31,82),(69,82))}},
    {"title":"Work in pairs","description":"Pair up along a court line. One partner leads with short lateral movements while the defender mirrors directly in front.","positions":{"d1":(28,43),"d2":(28,61),"d3":(50,43),"d4":(50,61),"d5":(72,43),"c":(72,61)},"pair_arrows":[((18,52),(38,52)),((40,52),(60,52)),((62,52),(82,52))]},
    {"title":"Switch leader and follower","description":"After 30 seconds, exchange roles and repeat with the same quickness, stance, spacing, and disciplined footwork."},
]


def gray_logo():
    source=Image.open(LOGO).convert("RGBA"); alpha=source.getchannel("A")
    gray=ImageEnhance.Contrast(ImageOps.grayscale(source.convert("RGB"))).enhance(1.45)
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
    lane_w,lane_h=w*.29,h*.38; lane_x=x+(w-lane_w)/2
    c.rect(lane_x,y,lane_w,lane_h,fill=0,stroke=1); c.circle(x+w/2,y+lane_h,lane_w/2,fill=0,stroke=1)
    c.setDash(3,3); c.arc(x+w/2-lane_w/2,y+lane_h-lane_w/2,x+w/2+lane_w/2,y+lane_h+lane_w/2,180,180); c.setDash()
    hoop_y=y+h*.115; c.setLineWidth(2); c.line(x+w*.42,hoop_y-h*.025,x+w*.58,hoop_y-h*.025)
    c.setLineWidth(1); c.circle(x+w/2,hoop_y,w*.022,fill=0,stroke=1); c.line(x+w*.09,y,x+w*.09,y+h*.20); c.line(x+w*.91,y,x+w*.91,y+h*.20); c.arc(x+w*.09,y-h*.08,x+w*.91,y+h*.67,12,156); c.restoreState()


def arrow(c,start,end,double=False):
    sx,sy=start; ex,ey=end; dx,dy=ex-sx,ey-sy; length=max((dx*dx+dy*dy)**.5,1)
    sx+=dx/length*8; sy+=dy/length*8; ex-=dx/length*8; ey-=dy/length*8; angle=atan2(ey-sy,ex-sx); head=5.5
    c.saveState(); c.setStrokeColorRGB(.05,.05,.05); c.setLineWidth(1.15); c.setDash(4,3); c.line(sx,sy,ex,ey); c.setDash()
    c.line(ex,ey,ex-head*cos(angle-pi/6),ey-head*sin(angle-pi/6)); c.line(ex,ey,ex-head*cos(angle+pi/6),ey-head*sin(angle+pi/6))
    if double:
        back=angle+pi; c.line(sx,sy,sx-head*cos(back-pi/6),sy-head*sin(back-pi/6)); c.line(sx,sy,sx-head*cos(back+pi/6),sy-head*sin(back+pi/6))
    c.restoreState()


def player(c,label,point,coach=False):
    x,y=point; c.saveState(); c.setFillColorRGB(.90,.90,.90) if coach else c.setFillColorRGB(1,1,1); c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.4); c.circle(x,y,7,fill=1,stroke=1)
    c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",7.5); c.drawCentredString(x,y-2.5,label); c.restoreState()


def draw_step(c,number,step,x,y,w,h,show_diagram=True):
    c.setStrokeColorRGB(.72,.72,.72); c.setLineWidth(.7); c.line(x,y,x+w,y)
    tx,tw=x+16,205; c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",11); c.drawString(tx,y+h-20,f"STEP {number}")
    draw_text(c,step["title"].upper(),tx,y+h-38,tw,size=10,leading=12,bold=True); draw_text(c,step["description"],tx,y+h-62,tw,size=8.2,leading=10.2)
    if not show_diagram:
        vx,vy=x+300,y+h-20; c.setFont("Helvetica-Bold",9); c.drawString(vx,vy,"VARIATIONS"); vy-=14
        for item in ["Use a coach-led line formation.","Pair players along a court line with one leader and one mirror."]:
            c.setFont("Helvetica-Bold",7); c.drawString(vx,vy,"-"); vy=draw_text(c,item,vx+9,vy,x+w-vx-9,size=7.2,leading=8.8)-2
        return
    court_w=125; court_h=court_w/(1090.86/912.61); court_x=x+w-16-court_w; court_y=y+(h-court_h)/2; draw_half_court(c,court_x,court_y,court_w,court_h)
    for motion in step.get("moves",{}).values(): arrow(c,pt(motion[0],court_x,court_y,court_w,court_h),pt(motion[1],court_x,court_y,court_w,court_h))
    for path in step.get("pair_arrows",[]): arrow(c,pt(path[0],court_x,court_y,court_w,court_h),pt(path[1],court_x,court_y,court_w,court_h),double=True)
    for pid,pos in step["positions"].items(): player(c,"C" if pid=="c" else pid[-1],pt(pos,court_x,court_y,court_w,court_h),coach=pid=="c")


def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1)
    c.setTitle("Mirror Drills - Decent.Coach Basket Ball Drills"); c.setAuthor("Decent.Coach"); c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96,.96,.96); c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0); c.drawImage(gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto")
    c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",15); c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills"); c.setFont("Helvetica",9); c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE")
    c.setFont("Helvetica-Bold",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"MIRROR DRILLS  |  1"); c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23); c.drawString(MARGIN,PAGE_H-101,"Mirror Drills"); c.setFont("Helvetica-Bold",9); c.drawString(MARGIN,PAGE_H-119,"DEFENSE  /  FOOTWORK  /  REACTION")
    c.setFont("Helvetica",9); draw_text(c,"Defenders mirror a leader's lateral movement while maintaining stance, spacing, and quick changes of direction.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12)
    c.setStrokeColorRGB(.65,.65,.65); c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151); c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176); c.setFont("Helvetica-Bold",8); c.drawString(MARGIN+10,PAGE_H-167,"5 PLAYERS + COACH   |   0 BALLS   |   HALF COURT")
    draw_step(c,1,STEPS[0],MARGIN,500,PAGE_W-2*MARGIN,115); draw_step(c,2,STEPS[1],MARGIN,385,PAGE_W-2*MARGIN,115); draw_step(c,3,STEPS[2],MARGIN,270,PAGE_W-2*MARGIN,115); draw_step(c,4,STEPS[3],MARGIN,155,PAGE_W-2*MARGIN,115); draw_step(c,5,STEPS[4],MARGIN,40,PAGE_W-2*MARGIN,115,show_diagram=False)
    c.setFont("Helvetica",7); c.drawRightString(PAGE_W-MARGIN,16,"decent.coach"); c.save(); print(OUTPUT)


if __name__=="__main__": create_pdf()
