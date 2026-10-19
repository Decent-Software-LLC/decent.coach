#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "print" / "line-running-drills.pdf"
LOGO = ROOT / "assets" / "branding" / "decent-basketball.png"
PAGE_W, PAGE_H = letter
MARGIN = 36

STEPS = [
    {
        "title": "Form four baseline lanes",
        "description": "Form four evenly spaced lanes from the baseline. The coach selects the running style and the stop or pivot for the repetition.",
        "positions": {"p1": (7,25), "p2": (7,42), "p3": (7,58), "p4": (7,75)},
    },
    {
        "title": "Run with controlled technique",
        "description": "The first player in each lane moves together using a normal jog, high heels, high knees, or grapevine.",
        "positions": {"p1": (34,25), "p2": (34,42), "p3": (34,58), "p4": (34,75)},
        "moves": {"p1": ((7,25),(34,25)), "p2": ((7,42),(34,42)), "p3": ((7,58),(34,58)), "p4": ((7,75),(34,75))},
    },
    {
        "title": "Stop and pivot on command",
        "description": "On the line or whistle, execute the selected jump stop, stride stop, forward pivot, reverse pivot, or hesitation step.",
        "positions": {"p1": (52,25), "p2": (52,42), "p3": (52,58), "p4": (52,75)},
        "moves": {"p1": ((34,25),(52,25)), "p2": ((34,42),(52,42)), "p3": ((34,58),(52,58)), "p4": ((34,75),(52,75))},
        "pivots": True,
    },
    {
        "title": "Finish through the court",
        "description": "Regain balance, push off, and finish through the far baseline while maintaining spacing across all four lanes.",
        "positions": {"p1": (91,25), "p2": (91,42), "p3": (91,58), "p4": (91,75)},
        "moves": {"p1": ((52,25),(91,25)), "p2": ((52,42),(91,42)), "p3": ((52,58),(91,58)), "p4": ((52,75),(91,75))},
    },
]


def gray_logo():
    source = Image.open(LOGO).convert("RGBA")
    alpha = source.getchannel("A")
    gray = ImageEnhance.Contrast(ImageOps.grayscale(source.convert("RGB"))).enhance(1.45)
    return ImageReader(Image.merge("RGBA", (gray, gray, gray, alpha)))


def wrap_lines(text, font, size, width):
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(c, text, x, y, width, size=9, leading=11, bold=False):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    for line in wrap_lines(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading


def pt(position, x, y, w, h):
    return x + position[0]/100*w, y + (1-position[1]/100)*h


def draw_full_court(c, x, y, w, h):
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(.08, .08, .08)
    c.setLineWidth(1)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.line(x+w/2, y, x+w/2, y+h)
    c.circle(x+w/2, y+h/2, h*.12, fill=0, stroke=1)
    lane_w = w*.18
    lane_h = h*.32
    c.rect(x, y+(h-lane_h)/2, lane_w, lane_h, fill=0, stroke=1)
    c.rect(x+w-lane_w, y+(h-lane_h)/2, lane_w, lane_h, fill=0, stroke=1)
    c.circle(x+lane_w, y+h/2, h*.11, fill=0, stroke=1)
    c.circle(x+w-lane_w, y+h/2, h*.11, fill=0, stroke=1)
    c.arc(x-w*.05, y+h*.12, x+w*.30, y+h*.88, -65, 130)
    c.arc(x+w*.70, y+h*.12, x+w*1.05, y+h*.88, 115, 130)
    c.setLineWidth(1.8)
    c.line(x+w*.035, y+h*.40, x+w*.035, y+h*.60)
    c.line(x+w*.965, y+h*.40, x+w*.965, y+h*.60)
    c.setLineWidth(1)
    c.circle(x+w*.055, y+h/2, 2.2, fill=0, stroke=1)
    c.circle(x+w*.945, y+h/2, 2.2, fill=0, stroke=1)
    c.restoreState()


def arrow(c, start, end, dashed=True):
    sx, sy = start
    ex, ey = end
    dx, dy = ex-sx, ey-sy
    length = max((dx*dx+dy*dy)**.5, 1)
    sx += dx/length*8
    sy += dy/length*8
    ex -= dx/length*9
    ey -= dy/length*9
    angle = atan2(ey-sy, ex-sx)
    c.saveState()
    c.setStrokeColorRGB(.06, .06, .06)
    c.setLineWidth(1.25)
    if dashed:
        c.setDash(4, 3)
    c.line(sx, sy, ex, ey)
    c.setDash()
    head = 5.5
    c.line(ex, ey, ex-head*cos(angle-pi/6), ey-head*sin(angle-pi/6))
    c.line(ex, ey, ex-head*cos(angle+pi/6), ey-head*sin(angle+pi/6))
    c.restoreState()


def draw_pivot(c, point):
    x, y = point
    c.saveState()
    c.setStrokeColorRGB(.05, .05, .05)
    c.setLineWidth(1)
    c.arc(x-9, y-9, x+9, y+9, 35, 245)
    angle = 35*pi/180
    ex, ey = x+9*cos(angle), y+9*sin(angle)
    c.line(ex, ey, ex-5*cos(angle+.45), ey-5*sin(angle+.45))
    c.line(ex, ey, ex-5*cos(angle-.45), ey-5*sin(angle-.45))
    c.restoreState()


def player(c, label, point):
    x, y = point
    c.saveState()
    c.setFillColorRGB(.08, .08, .08)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.2)
    c.circle(x, y, 7, fill=1, stroke=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x, y-2.5, label)
    c.restoreState()


def draw_step(c, number, step, x, y, w, h):
    c.setStrokeColorRGB(.72, .72, .72)
    c.setLineWidth(.7)
    c.line(x, y, x+w, y)
    text_x, text_w = x+16, 210
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(text_x, y+h-22, f"STEP {number}")
    draw_text(c, step["title"].upper(), text_x, y+h-41, text_w, size=10, leading=12, bold=True)
    draw_text(c, step["description"], text_x, y+h-68, text_w, size=8.5, leading=10.5)

    court_w, court_h = 166, 100
    court_x = x+w-16-court_w
    court_y = y+(h-court_h)/2
    draw_full_court(c, court_x, court_y, court_w, court_h)
    for motion in step.get("moves", {}).values():
        arrow(c, pt(motion[0], court_x, court_y, court_w, court_h), pt(motion[1], court_x, court_y, court_w, court_h))
    for pid, position in step["positions"].items():
        point = pt(position, court_x, court_y, court_w, court_h)
        if step.get("pivots"):
            draw_pivot(c, point)
        player(c, pid[-1], point)


def create_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("Lane Running Drills - Decent.Coach Basket Ball Drills")
    c.setAuthor("Decent.Coach")
    c.setSubject("Printable basketball drill coaching guide")
    c.setFillColorRGB(.96, .96, .96)
    c.rect(0, PAGE_H-68, PAGE_W, 68, fill=1, stroke=0)
    c.drawImage(gray_logo(), MARGIN, PAGE_H-58, 42, 42, mask="auto")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN+52, PAGE_H-33, "Decent.Coach Basket Ball Drills")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN+52, PAGE_H-48, "PRINTABLE COACHING GUIDE")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W-MARGIN, PAGE_H-39, "LANE RUNNING DRILLS  |  1")
    c.line(MARGIN, PAGE_H-68, PAGE_W-MARGIN, PAGE_H-68)

    c.setFont("Helvetica-Bold", 23)
    c.drawString(MARGIN, PAGE_H-101, "Lane Running Drills")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H-119, "FOOTWORK  /  MOVEMENT  /  BALANCE")
    c.setFont("Helvetica", 9)
    draw_text(c, "Four lanes cross the court using a selected running style, then execute controlled stops, pivots, and changes of direction.", MARGIN, PAGE_H-139, PAGE_W-2*MARGIN, size=9, leading=12)
    c.setStrokeColorRGB(.65, .65, .65)
    c.line(MARGIN, PAGE_H-151, PAGE_W-MARGIN, PAGE_H-151)
    c.line(MARGIN, PAGE_H-176, PAGE_W-MARGIN, PAGE_H-176)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN+10, PAGE_H-167, "ALL PLAYERS   |   0 BALLS   |   FULL COURT")

    draw_step(c, 1, STEPS[0], MARGIN, 468, PAGE_W-2*MARGIN, 147)
    draw_step(c, 2, STEPS[1], MARGIN, 321, PAGE_W-2*MARGIN, 147)
    draw_step(c, 3, STEPS[2], MARGIN, 174, PAGE_W-2*MARGIN, 147)
    draw_step(c, 4, STEPS[3], MARGIN, 27, PAGE_W-2*MARGIN, 147)

    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(MARGIN+16, 43, "VARIATION")
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN+72, 43, "Use follow-the-leader with one player choosing each movement.")
    c.setFont("Helvetica", 7)
    c.drawRightString(PAGE_W-MARGIN, 16, "decent.coach")
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    create_pdf()
