#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "print" / "defensive-shuffle-and-pass.pdf"
LOGO = ROOT / "assets" / "branding" / "decent-basketball.png"
PAGE_W, PAGE_H = letter
MARGIN = 36

STEPS = [
    {
        "title": "Set up the triangle",
        "description": "Two passers begin three to four steps apart. The worker faces Player 1 in a low defensive stance.",
        "positions": {"p1": (35, 72), "p2": (65, 72), "p3": (35, 42)},
        "ball": "p1",
    },
    {
        "title": "Pass and return",
        "description": "Player 1 passes to the worker. The worker returns a crisp pass while staying balanced and ready to move.",
        "positions": {"p1": (35, 72), "p2": (65, 72), "p3": (35, 42)},
        "ball": "p1",
        "pass_exchange": ((35, 72), (35, 42)),
    },
    {
        "title": "Shuffle to the second passer",
        "description": "Stay low and shuffle wide-to-wider until positioned in front of Player 2. Do not cross the feet.",
        "positions": {"p1": (35, 72), "p2": (65, 72), "p3": (65, 42)},
        "ball": "p2",
        "moves": {"p3": ((35, 42), (65, 42))},
    },
    {
        "title": "Return and repeat",
        "description": "Exchange a crisp pass with Player 2, then shuffle back toward Player 1 and continue the sequence.",
        "positions": {"p1": (35, 72), "p2": (65, 72), "p3": (35, 42)},
        "ball": "p2",
        "pass_exchange": ((65, 72), (65, 42)),
        "moves": {"p3": ((65, 42), (35, 42))},
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
    c.arc(x+w/2-lane_w/2, y+lane_h-lane_w/2, x+w/2+lane_w/2, y+lane_h+lane_w/2, 180, 180)
    c.setDash()
    hoop_y = y + h * .115
    c.setLineWidth(2)
    c.line(x+w*.42, hoop_y-h*.025, x+w*.58, hoop_y-h*.025)
    c.setLineWidth(1)
    c.circle(x+w/2, hoop_y, w*.022, fill=0, stroke=1)
    c.line(x+w*.09, y, x+w*.09, y+h*.20)
    c.line(x+w*.91, y, x+w*.91, y+h*.20)
    c.arc(x+w*.09, y-h*.08, x+w*.91, y+h*.67, 12, 156)
    c.restoreState()


def arrow(c, start, end, dashed=False, curve=0, width=1.3, end_trim=0, double_ended=False):
    sx, sy = start
    ex, ey = end
    dx, dy = ex-sx, ey-sy
    length = max((dx*dx + dy*dy) ** .5, 1)
    if end_trim:
        if double_ended:
            sx += dx/length * end_trim
            sy += dy/length * end_trim
        ex -= dx/length * end_trim
        ey -= dy/length * end_trim
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
    if double_ended:
        start_angle = atan2(sy-cy, sx-cx)
        c.line(sx, sy, sx-head*cos(start_angle-pi/6), sy-head*sin(start_angle-pi/6))
        c.line(sx, sy, sx-head*cos(start_angle+pi/6), sy-head*sin(start_angle+pi/6))
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

    for motion in step.get("moves", {}).values():
        arrow(c, pt(motion[0], court_x, court_y, court_w, court_h), pt(motion[1], court_x, court_y, court_w, court_h), dashed=True, curve=0, end_trim=10)
    if step.get("pass_exchange"):
        pass_path = step["pass_exchange"]
        arrow(c, pt(pass_path[0], court_x, court_y, court_w, court_h), pt(pass_path[1], court_x, court_y, court_w, court_h), width=1.8, end_trim=10, double_ended=True)

    for pid, position in step["positions"].items():
        team = "defense" if pid == "p3" else "offense"
        label = {"p1":"1", "p2":"2", "p3":"X3"}[pid]
        player(c, label, team, pt(position, court_x, court_y, court_w, court_h), has_ball=pid in {"p1", "p2"})


def create_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("Defensive Shuffle And Pass - Decent.Coach Basket Ball Drills")
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
    c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(PAGE_W-MARGIN, PAGE_H-39, "DEFENSIVE SHUFFLE AND PASS  |  1")
    c.line(MARGIN, PAGE_H-68, PAGE_W-MARGIN, PAGE_H-68)

    c.setFont("Helvetica-Bold", 23)
    c.drawString(MARGIN, PAGE_H-101, "Defensive Shuffle And Pass")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H-119, "DEFENSE  /  PASSING  /  FOOTWORK")
    c.setFont("Helvetica", 9)
    draw_text(c, "Three players combine crisp passing with repeated defensive shuffles between two ball-handlers.", MARGIN, PAGE_H-139, PAGE_W-2*MARGIN, size=9, leading=12)
    c.setStrokeColorRGB(.65, .65, .65)
    c.line(MARGIN, PAGE_H-151, PAGE_W-MARGIN, PAGE_H-151)
    c.line(MARGIN, PAGE_H-176, PAGE_W-MARGIN, PAGE_H-176)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN+10, PAGE_H-167, "3 PLAYERS   |   2 BALLS   |   HALF COURT")

    draw_step(c, 1, STEPS[0], MARGIN, 468, PAGE_W-2*MARGIN, 147)
    draw_step(c, 2, STEPS[1], MARGIN, 321, PAGE_W-2*MARGIN, 147)
    draw_step(c, 3, STEPS[2], MARGIN, 174, PAGE_W-2*MARGIN, 147)
    draw_step(c, 4, STEPS[3], MARGIN, 27, PAGE_W-2*MARGIN, 147)

    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(MARGIN+16, 43, "VARIATIONS")
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN+78, 43, "Specify the pass type, or count completed passes during a timed round.")
    c.setFont("Helvetica", 7)
    c.drawRightString(PAGE_W-MARGIN, 16, "decent.coach")
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    create_pdf()
