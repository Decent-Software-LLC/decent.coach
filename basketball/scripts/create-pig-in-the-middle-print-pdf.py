#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "print" / "pig-in-the-middle.pdf"
LOGO = ROOT / "assets" / "branding" / "decent-basketball.png"
PAGE_W, PAGE_H = letter
MARGIN = 36

STEPS = [
    {
        "title": "Set a three-player group",
        "description": "Two passers face each other with one defender between them. Player 1 starts with the ball.",
        "positions": {"o1": (30, 55), "o2": (70, 55), "d1": (50, 55)},
        "ball": "o1",
    },
    {
        "title": "Pressure the ball",
        "description": "The defender closes aggressively and calls 'ball.' The passer protects the ball and uses a strong pass fake.",
        "positions": {"o1": (30, 55), "o2": (70, 55), "d1": (39, 55)},
        "ball": "o1",
        "moves": {"d1": ((50, 55), (39, 55))},
        "callout": "BALL",
    },
    {
        "title": "Create and complete the pass",
        "description": "The passer steps into or around pressure. The defender attacks the passing lane, then recovers to pressure the receiver.",
        "positions": {"o1": (27, 52), "o2": (70, 55), "d1": (59, 55)},
        "ball": "o2",
        "pass": ((30, 55), (70, 55)),
        "moves": {"o1": ((30, 55), (27, 52)), "d1": ((39, 55), (59, 55))},
        "callout": "BALL",
    },
    {
        "title": "Deflect and exchange roles",
        "description": "When the defender touches or intercepts a pass, exchange roles with the passer and continue immediately.",
        "positions": {"o1": (50, 55), "o2": (70, 55), "d1": (30, 55)},
        "ball": "d1",
        "pass": ((70, 55), (49, 54)),
        "moves": {"o1": ((27, 52), (50, 55)), "d1": ((59, 55), (30, 55))},
        "swapped": True,
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
    return y


def pt(position, x, y, w, h):
    return x + position[0] / 100 * w, y + (1 - position[1] / 100) * h


def draw_half_court(c, x, y, w, h):
    c.saveState()
    c.setStrokeColorRGB(.08, .08, .08)
    c.setFillColorRGB(1, 1, 1)
    c.setLineWidth(1)
    c.rect(x, y, w, h, fill=1, stroke=1)
    lane_w, lane_h = w * .29, h * .38
    lane_x = x + (w - lane_w) / 2
    c.rect(lane_x, y, lane_w, lane_h, fill=0, stroke=1)
    c.circle(x + w / 2, y + lane_h, lane_w / 2, fill=0, stroke=1)
    c.setDash(3, 3)
    c.arc(x + w/2-lane_w/2, y+lane_h-lane_w/2, x+w/2+lane_w/2, y+lane_h+lane_w/2, 180, 180)
    c.setDash()
    hoop_y = y + h * .115
    c.setLineWidth(2)
    c.line(x + w*.42, hoop_y-h*.025, x+w*.58, hoop_y-h*.025)
    c.setLineWidth(1)
    c.circle(x+w/2, hoop_y, w*.022, fill=0, stroke=1)
    c.line(x+w*.09, y, x+w*.09, y+h*.20)
    c.line(x+w*.91, y, x+w*.91, y+h*.20)
    c.arc(x+w*.09, y-h*.08, x+w*.91, y+h*.67, 12, 156)
    c.restoreState()


def arrow(c, start, end, dashed=False, curve=0, width=1.25):
    sx, sy = start
    ex, ey = end
    dx, dy = ex-sx, ey-sy
    length = max((dx*dx + dy*dy) ** .5, 1)
    nx, ny = -dy/length, dx/length
    cx, cy = (sx+ex)/2 + nx*curve, (sy+ey)/2 + ny*curve
    c.saveState()
    c.setStrokeColorRGB(.05, .05, .05)
    c.setLineWidth(width)
    if dashed:
        c.setDash(4, 3)
    path = c.beginPath()
    path.moveTo(sx, sy)
    path.curveTo(cx, cy, cx, cy, ex, ey)
    c.drawPath(path, stroke=1, fill=0)
    c.setDash()
    angle = atan2(ey-cy, ex-cx)
    head = 6
    c.line(ex, ey, ex-head*cos(angle-pi/6), ey-head*sin(angle-pi/6))
    c.line(ex, ey, ex-head*cos(angle+pi/6), ey-head*sin(angle+pi/6))
    c.restoreState()


def player(c, label, team, point, has_ball=False):
    x, y = point
    radius = 8
    c.saveState()
    c.setLineWidth(1.4)
    if team == "offense":
        c.setFillColorRGB(.08, .08, .08)
        c.circle(x, y, radius, fill=1, stroke=1)
        c.setFillColorRGB(1, 1, 1)
    else:
        c.setFillColorRGB(1, 1, 1)
        c.circle(x, y, radius, fill=1, stroke=1)
        c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 7 if len(label) > 1 else 8)
    c.drawCentredString(x, y-2.5, label)
    if has_ball:
        c.setFillColorRGB(0, 0, 0)
        c.circle(x+7, y+7, 3.5, fill=1, stroke=0)
    c.restoreState()


def callout(c, text, point):
    x, y = point
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(x-15, y+14, 30, 12, fill=1, stroke=1)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(x, y+17, text)
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

    court_w = 142
    court_h = court_w / (1090.86 / 912.61)
    court_x = x+w-16-court_w
    court_y = y+(h-court_h)/2
    draw_half_court(c, court_x, court_y, court_w, court_h)

    for pid, motion in step.get("moves", {}).items():
        arrow(c, pt(motion[0], court_x, court_y, court_w, court_h), pt(motion[1], court_x, court_y, court_w, court_h), dashed=pid == "d1", curve=7 if pid == "d1" else -6)
    if step.get("pass"):
        arrow(c, pt(step["pass"][0], court_x, court_y, court_w, court_h), pt(step["pass"][1], court_x, court_y, court_w, court_h), width=2)

    swapped = step.get("swapped", False)
    for pid, position in step["positions"].items():
        offense = pid.startswith("o")
        team = "defense" if offense == swapped else "offense"
        label = {"o1":"1", "o2":"2", "d1":"X1"}[pid]
        point = pt(position, court_x, court_y, court_w, court_h)
        player(c, label, team, point, has_ball=pid == step["ball"])
        if pid == "d1" and step.get("callout"):
            callout(c, step["callout"], point)


def create_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("Pig In The Middle - Decent.Coach Basket Ball Drills")
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
    c.drawRightString(PAGE_W-MARGIN, PAGE_H-39, "PIG IN THE MIDDLE  |  1")
    c.line(MARGIN, PAGE_H-68, PAGE_W-MARGIN, PAGE_H-68)

    c.setFont("Helvetica-Bold", 23)
    c.drawString(MARGIN, PAGE_H-101, "Pig In The Middle")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H-119, "PASSING  /  BALL PRESSURE  /  DEFLECTIONS")
    c.setFont("Helvetica", 9)
    draw_text(c, "Two passers protect the ball while one defender pressures the ball and attacks the passing lane.", MARGIN, PAGE_H-139, PAGE_W-2*MARGIN, size=9, leading=12)
    c.setStrokeColorRGB(.65, .65, .65)
    c.line(MARGIN, PAGE_H-151, PAGE_W-MARGIN, PAGE_H-151)
    c.line(MARGIN, PAGE_H-176, PAGE_W-MARGIN, PAGE_H-176)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN+10, PAGE_H-167, "3 PLAYERS   |   1 BALL   |   HALF COURT")

    draw_step(c, 1, STEPS[0], MARGIN, 468, PAGE_W-2*MARGIN, 147)
    draw_step(c, 2, STEPS[1], MARGIN, 321, PAGE_W-2*MARGIN, 147)
    draw_step(c, 3, STEPS[2], MARGIN, 174, PAGE_W-2*MARGIN, 147)
    draw_step(c, 4, STEPS[3], MARGIN, 27, PAGE_W-2*MARGIN, 147)

    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(MARGIN+16, 43, "VARIATION")
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN+72, 43, "Give each passer a three-second limit to release the ball.")
    c.setFont("Helvetica", 7)
    c.drawRightString(PAGE_W-MARGIN, 16, "decent.coach")
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    create_pdf()
