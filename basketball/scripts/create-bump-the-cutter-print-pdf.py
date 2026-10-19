#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"print"/"bump-the-cutter.pdf"
LOGO=ROOT/"assets"/"branding"/"decent-basketball.png"
PAGE_W,PAGE_H=letter
MARGIN=36

STEPS=[
    {"title":"See ball and cutter","description":"The coach starts outside the arc with the ball. The cutter begins opposite while the defender establishes a flat-triangle position.","positions":{"c":(80,55),"o":(18,24),"d":(50,46)},"ball":"c"},
    {"title":"Meet the flash cut","description":"As the cutter flashes toward the ball, the defender stays lower, meets the cut in the lane, and makes legal contact.","positions":{"c":(80,55),"o":(46,39),"d":(53,42)},"ball":"c","moves":{"o":((18,24),(46,39)),"d":((50,46),(53,42))}},
    {"title":"Deny and force the cutter out","description":"Deny the pass inside the key and force the cutter toward a less advantageous catch away from the basket.","positions":{"c":(80,55),"o":(51,73),"d":(58,64)},"ball":"c","moves":{"o":((46,39),(51,73)),"d":((53,42),(58,64))}},
    {"title":"Play live on the catch","description":"If the cutter receives the pass, play one-on-one to the basket. Limit the offensive player to two dribbles.","positions":{"c":(80,55),"o":(50,24),"d":(56,28)},"ball":"o","pass":((80,55),(51,73)),"moves":{"o":((51,73),(50,24)),"d":((58,64),(56,28))}},
    {"title":"Rotate offense to defense","description":"After the repetition, the offensive player becomes the defender and the defender becomes the next cutter."},
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


def arrow(c,start,end,dashed=False,curve=0,width=1.3):
    sx,sy=start; ex,ey=end; dx,dy=ex-sx,ey-sy; length=max((dx*dx+dy*dy)**.5,1); sx+=dx/length*9; sy+=dy/length*9; ex-=dx/length*9; ey-=dy/length*9
    nx,ny=-dy/length,dx/length; cx,cy=(sx+ex)/2+nx*curve,(sy+ey)/2+ny*curve
    c.saveState(); c.setStrokeColorRGB(.05,.05,.05); c.setLineWidth(width)
    if dashed: c.setDash(4,3)
    path=c.beginPath(); path.moveTo(sx,sy); path.curveTo(cx,cy,cx,cy,ex,ey); c.drawPath(path,stroke=1,fill=0); c.setDash(); angle=atan2(ey-cy,ex-cx); head=5.5
    c.line(ex,ey,ex-head*cos(angle-pi/6),ey-head*sin(angle-pi/6)); c.line(ex,ey,ex-head*cos(angle+pi/6),ey-head*sin(angle+pi/6)); c.restoreState()


def player(c,label,point,role,ball=False):
    x,y=point; c.saveState(); c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.3)
    if role=="offense": c.setFillColorRGB(.08,.08,.08); c.circle(x,y,8,fill=1,stroke=1); c.setFillColorRGB(1,1,1)
    elif role=="defense": c.setFillColorRGB(1,1,1); c.circle(x,y,8,fill=1,stroke=1); c.setFillColorRGB(0,0,0)
    else: c.setFillColorRGB(.86,.86,.86); c.circle(x,y,8,fill=1,stroke=1); c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica-Bold",7.5); c.drawCentredString(x,y-2.5,label)
    if ball: c.setFillColorRGB(0,0,0); c.circle(x+7,y+7,3.5,fill=1,stroke=0)
    c.restoreState()


def draw_step(c,number,step,x,y,w,h,show_diagram=True):
    c.setStrokeColorRGB(.72,.72,.72); c.setLineWidth(.7); c.line(x,y,x+w,y); tx,tw=x+16,205; c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",11); c.drawString(tx,y+h-20,f"STEP {number}")
    draw_text(c,step["title"].upper(),tx,y+h-38,tw,size=10,leading=12,bold=True); draw_text(c,step["description"],tx,y+h-62,tw,size=8.2,leading=10.2)
    if not show_diagram:
        vx,vy=x+300,y+h-20; c.setFont("Helvetica-Bold",9); c.drawString(vx,vy,"VARIATION"); vy-=14; c.setFont("Helvetica-Bold",7); c.drawString(vx,vy,"-"); draw_text(c,"Reposition the coach and cutter in different areas of the offensive half court.",vx+9,vy,x+w-vx-9,size=7.2,leading=8.8); return
    court_w=125; court_h=court_w/(1090.86/912.61); court_x=x+w-16-court_w; court_y=y+(h-court_h)/2; draw_half_court(c,court_x,court_y,court_w,court_h)
    for pid,motion in step.get("moves",{}).items(): arrow(c,pt(motion[0],court_x,court_y,court_w,court_h),pt(motion[1],court_x,court_y,court_w,court_h),dashed=pid=="d",curve=6 if pid=="d" else -6)
    if step.get("pass"): arrow(c,pt(step["pass"][0],court_x,court_y,court_w,court_h),pt(step["pass"][1],court_x,court_y,court_w,court_h),width=1.8)
    roles={"c":("C","neutral"),"o":("1","offense"),"d":("X","defense")}
    for pid,pos in step["positions"].items():
        label,role=roles[pid]; player(c,label,pt(pos,court_x,court_y,court_w,court_h),role,ball=pid==step["ball"])


def create_pdf():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); c=canvas.Canvas(str(OUTPUT),pagesize=letter,pageCompression=1); c.setTitle("Bump The Cutter - Decent.Coach Basket Ball Drills"); c.setAuthor("Decent.Coach"); c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96,.96,.96); c.rect(0,PAGE_H-68,PAGE_W,68,fill=1,stroke=0); c.drawImage(gray_logo(),MARGIN,PAGE_H-58,42,42,mask="auto"); c.setFillColorRGB(0,0,0); c.setFont("Helvetica-Bold",15); c.drawString(MARGIN+52,PAGE_H-33,"Decent.Coach Basket Ball Drills"); c.setFont("Helvetica",9); c.drawString(MARGIN+52,PAGE_H-48,"PRINTABLE COACHING GUIDE"); c.setFont("Helvetica-Bold",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-39,"BUMP THE CUTTER  |  1"); c.line(MARGIN,PAGE_H-68,PAGE_W-MARGIN,PAGE_H-68)
    c.setFont("Helvetica-Bold",23); c.drawString(MARGIN,PAGE_H-101,"Bump The Cutter"); c.setFont("Helvetica-Bold",9); c.drawString(MARGIN,PAGE_H-119,"DEFENSE  /  DENIAL  /  FOOTWORK"); c.setFont("Helvetica",9); draw_text(c,"A defender reads ball and cutter, meets the flash cut in the lane, and denies an easy catch in the key.",MARGIN,PAGE_H-139,PAGE_W-2*MARGIN,size=9,leading=12)
    c.setStrokeColorRGB(.65,.65,.65); c.line(MARGIN,PAGE_H-151,PAGE_W-MARGIN,PAGE_H-151); c.line(MARGIN,PAGE_H-176,PAGE_W-MARGIN,PAGE_H-176); c.setFont("Helvetica-Bold",8); c.drawString(MARGIN+10,PAGE_H-167,"3 PLAYERS   |   1 BALL   |   HALF COURT")
    draw_step(c,1,STEPS[0],MARGIN,500,PAGE_W-2*MARGIN,115); draw_step(c,2,STEPS[1],MARGIN,385,PAGE_W-2*MARGIN,115); draw_step(c,3,STEPS[2],MARGIN,270,PAGE_W-2*MARGIN,115); draw_step(c,4,STEPS[3],MARGIN,155,PAGE_W-2*MARGIN,115); draw_step(c,5,STEPS[4],MARGIN,40,PAGE_W-2*MARGIN,115,show_diagram=False)
    c.setFont("Helvetica",7); c.drawRightString(PAGE_W-MARGIN,16,"decent.coach"); c.save(); print(OUTPUT)


if __name__=="__main__": create_pdf()
