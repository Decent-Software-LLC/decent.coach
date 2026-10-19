#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"print"/"bull-in-the-ring.pdf"
LOGO=ROOT/"assets"/"branding"/"decent-basketball.png"
PAGE_W,PAGE_H=letter
MARGIN=36

RING={"o1":(50,24),"o2":(33,31),"o3":(23,47),"o4":(29,68),"o5":(50,78),"o6":(71,68),"o7":(77,47),"o8":(67,31)}
STEPS=[
    {"title":"Form the ring","description":"Form a wide circle around one defender. One outside player starts with the ball and may pass to any non-adjacent player.","positions":{**RING,"d1":(50,50)},"ball":"o1"},
    {"title":"Fake, pass, and pressure","description":"The ball carrier uses a pass fake, then passes to any eligible player around the ring. The defender pressures the ball and attacks the lane.","positions":{**RING,"d1":(39,39)},"ball":"o3","pass":((50,24),(23,47)),"move":((50,50),(39,39))},
    {"title":"Recover to the next pass","description":"The new ball carrier quickly passes to any other eligible player around the ring. The defender recovers and keeps active hands.","positions":{**RING,"d1":(50,58)},"ball":"o6","pass":((23,47),(71,68)),"move":((39,39),(50,58))},
    {"title":"Touch the pass and rotate","description":"On a touch or interception, the passer becomes the new defender and the former defender joins the outside ring.","positions":{"o1":(50,24),"o2":(33,31),"o3":(23,47),"o4":(29,68),"o5":(50,78),"o6":(50,50),"o7":(77,47),"o8":(67,31),"d1":(71,68)},"ball":"d1","move":((50,58),(71,68)),"swap":((71,68),(50,50))},
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
    lane_w,lane_h=w*.29,h*.38; lane_x=x+(w-lane_w)/2; c.rect(lane_x,y,lane_w,lane_h,fill=0,stroke=1); c.circle(x+w/2,y+lane_h,lane_w/2,fill=0,stroke=1)
    c.setDash(3,3); c.arc(x+w/2-lane_w/2,y+lane_h-lane_w/2,x+w/2+lane_w/2,y+lane_h+lane_w/2,180,180); c.setDash()
    hoop_y=y+h*.115; c.setLineWidth(2); c.line(x+w*.42,hoop_y-h*.025,x+w*.58,hoop_y-h*.025); c.setLineWidth(1); c.circle(x+w/2,hoop_y,w*.022,fill=0,stroke=1)
    c.line(x+w*.09,y,x+w*.09,y+h*.20); c.line(x+w*.91,y,x+w*.91,y+h*.20); c.arc(x+w*.09,y-h*.08,x+w*.91,y+h*.67,12,156); c.restoreState()


def arrow(c,start,end,dashed=False,curve=0,width=1.3):
    sx,sy=start; ex,ey=end; dx,dy=ex-sx,ey-sy; length=max((dx*dx+dy*dy)**.5,1); sx+=dx/length*8; sy+=dy/length*8; ex-=dx/length*8; ey-=dy/length*8
    nx,ny=-dy/length,dx/length; cx,cy=(sx+ex)/2+nx*curve,(sy+ey)/2+ny*curve
    c.saveState(); c.setStrokeColorRGB(.05,.05,.05); c.setLineWidth(width)
    if dashed: c.setDash(4,3)
    path=c.beginPath(); path.moveTo(sx,sy); path.curveTo(cx,cy,cx,cy,ex,ey); c.drawPath(path,stroke=1,fill=0); c.setDash(); angle=atan2(ey-cy,ex-cx); head=5.5
    c.line(ex,ey,ex-head*cos(angle-pi/6),ey-head*sin(angle-pi/6)); c.line(ex,ey,ex-head*cos(angle+pi/6),ey-head*sin(angle+pi/6)); c.restoreState()


def player(c,label,point,defense=False,ball=False):
    x,y=point; c.saveState(); c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.2)
    if defense: c.setFillColorRGB(1,1,1); c.circle(x,y,6.5,fill=1,stroke=1); c.setFillColorRGB(0,0,0)
    else: c.setFillColorRGB(.08,.08,.08); c.circle(x,y,6.5,fill=1,stroke=1); c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold",6.8); c.drawCentredString(x,y-2.2,label)
    if ball: c.setFillColorRGB(0,0,0); c.circle(x+6,y+6,3,fill=1,stroke=0)
    c.restoreState()


def draw_step(c,number,step,x,y,w,h):
    c.setStrokeColorRGB(.72,.72,.72); c.setLineWidth(.7); c.line(x,y,x+w,y); tx,tw=x+16,210
    c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",11); c.drawString(tx,y+h-22,f"STEP {number}"); draw_text(c,step["title"].upper(),tx,y+h-41,tw,size=10,leading=12,bold=True); draw_text(c,step["description"],tx,y+h-68,tw,size=8.5,leading=10.5)
    court_w=142; court_h=court_w/(1090.86/912.61); court_x=x+w-16-court_w; court_y=y+(h-court_h)/2; draw_half_court(c,court_x,court_y,court_w,court_h)
    if step.get("pass"): arrow(c,pt(step["pass"][0],court_x,court_y,court_w,court_h),pt(step["pass"][1],court_x,court_y,court_w,court_h),width=1.8)
    if step.get("move"): arrow(c,pt(step["move"][0],court_x,court_y,court_w,court_h),pt(step["move"][1],court_x,court_y,court_w,court_h),dashed=True,curve=6)
    if step.get("swap"): arrow(c,pt(step["swap"][0],court_x,court_y,court_w,court_h),pt(step["swap"][1],court_x,court_y,court_w,court_h),dashed=True,curve=-6)
    for pid,pos in step["positions"].items():
        defense=(pid=="d1" and number<4) or (pid=="o6" and number==4); label="X" if pid=="d1" else pid[-1]
        player(c,label,pt(pos,court_x,court_y,court_w,court_h),defense=defense,ball=pid==step["ball"])
    if number==4:
        c.setFont("Helvetica-Bold",7.5); c.drawString(tx,43,"VARIATIONS")
        c.setFont("Helvetica",7.2); c.drawString(tx+62,43,"Add balls or defenders; resize the ring; use a three-second pass limit.")


def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1); c.setTitle("Bull In The Ring - Decent.Coach Basket Ball Drills"); c.setAuthor("Decent.Coach"); c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96,.96,.96); c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0); c.drawImage(gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto"); c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",15); c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills"); c.setFont("Helvetica",9); c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE"); c.setFont("Helvetica-Bold",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"BULL IN THE RING  |  1"); c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23); c.drawString(MARGIN,PAGE_H-101,"Bull In The Ring"); c.setFont("Helvetica-Bold",9); c.drawString(MARGIN,PAGE_H-119,"PASSING  /  DEFENSE  /  BALL PRESSURE"); c.setFont("Helvetica",9); draw_text(c,"Players pass across a circle while one defender pressures the ball and hunts for a touch or interception.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12)
    c.setStrokeColorRGB(.65,.65,.65); c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151); c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176); c.setFont("Helvetica-Bold",8); c.drawString(MARGIN+10,PAGE_H-167,"ALL PLAYERS   |   1 BALL   |   HALF COURT")
    draw_step(c,1,STEPS[0],MARGIN,468,PAGE_W-2*MARGIN,147); draw_step(c,2,STEPS[1],MARGIN,321,PAGE_W-2*MARGIN,147); draw_step(c,3,STEPS[2],MARGIN,174,PAGE_W-2*MARGIN,147); draw_step(c,4,STEPS[3],MARGIN,27,PAGE_W-2*MARGIN,147)
    c.setFont("Helvetica",7); c.drawRightString(PAGE_W-MARGIN,16,"decent.coach"); c.save(); print(OUTPUT)


if __name__=="__main__": create_pdf()
