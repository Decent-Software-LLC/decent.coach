#!/usr/bin/env python3
from math import atan2, cos, pi, sin
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "print" / "shell-drill.pdf"
LOGO = ROOT / "assets" / "branding" / "decent-basketball.png"
PAGE_W, PAGE_H = letter
MARGIN = 36

OFFENSE = {"o1": "1", "o2": "2", "o3": "3", "o4": "4"}
DEFENSE = {"d1": "X1", "d2": "X2", "d3": "X3", "d4": "X4"}

STEPS = [
    {
        "title": "Set the shell",
        "description": "Pressure the ball. One pass away, deny. On the weak side, drop to help and see both ball and player.",
        "positions": {"o1":(38,27),"o2":(62,27),"o3":(12,48),"o4":(88,48),"d1":(42,40),"d2":(54,38),"d3":(30,52),"d4":(50,55)},
        "ball": "o1",
        "callouts": {"d1":"BALL", "d2":"DENY", "d3":"DENY", "d4":"HELP"},
        "moves": {},
    },
    {
        "title": "Fly with the first pass",
        "description": "On the pass, the new on-ball defender closes out. One pass away, deny. Weak-side defenders drop to help.",
        "positions": {"o1":(38,27),"o2":(62,27),"o3":(12,48),"o4":(88,48),"d1":(46,38),"d2":(58,40),"d3":(50,55),"d4":(70,52)},
        "ball": "o2",
        "pass": ("o1", "o2"),
        "callouts": {"d1":"DENY", "d2":"BALL", "d3":"HELP", "d4":"DENY"},
        "moves": {"d1":((42,40),(46,38)),"d2":((54,38),(58,40)),"d3":((30,52),(50,55)),"d4":((50,55),(70,52))},
    },
    {
        "title": "Shift to the wing",
        "description": "As the ball moves to the wing, close out to the ball. One pass away, deny. Weak-side defenders drop to help and find the split line.",
        "positions": {"o1":(38,27),"o2":(62,27),"o3":(12,48),"o4":(88,48),"d1":(50,52),"d2":(67,46),"d3":(47,56),"d4":(72,60)},
        "ball": "o4",
        "pass": ("o2", "o4"),
        "callouts": {"d1":"SPLIT", "d2":"DENY", "d3":"HELP", "d4":"BALL"},
        "moves": {"d1":((46,38),(50,52)),"d2":((58,40),(67,46)),"d3":((50,55),(47,56)),"d4":((70,52),(72,60))},
    },
    {
        "title": "Help across the shell",
        "description": "As the ball reverses, close out to the ball. One pass away, deny. Weak-side defenders drop to help while seeing ball and player.",
        "positions": {"o1":(38,27),"o2":(62,27),"o3":(12,48),"o4":(88,48),"d1":(33,46),"d2":(50,52),"d3":(28,60),"d4":(53,56)},
        "ball": "o3",
        "pass": ("o4", "o3"),
        "callouts": {"d1":"DENY", "d2":"HELP", "d3":"BALL", "d4":"HELP"},
        "moves": {"d1":((50,52),(33,46)),"d2":((67,46),(50,52)),"d3":((47,56),(28,60)),"d4":((72,60),(53,56))},
    },
    {
        "title": "Rotate and progress",
        "description": "Switch offense and defense. Repeat, then progress to cuts, denial, penetration, screens, and live four-on-four.",
        "positions": {"o1":(42,40),"o2":(54,38),"o3":(30,52),"o4":(50,55),"d1":(38,34),"d2":(62,34),"d3":(22,56),"d4":(78,56)},
        "ball": "d1",
        "teams_swapped": True,
        "moves": {
            "o1":((38,34),(42,40)),"o2":((62,34),(54,38)),"o3":((22,56),(30,52)),"o4":((78,56),(50,55)),
            "d1":((33,46),(38,34)),"d2":((50,52),(62,34)),"d3":((28,60),(22,56)),"d4":((53,56),(78,56)),
        },
    },
]


def grayscale_logo():
    source = Image.open(LOGO).convert("RGBA")
    alpha = source.getchannel("A")
    gray = ImageOps.grayscale(source.convert("RGB"))
    gray = ImageEnhance.Contrast(gray).enhance(1.45)
    result = Image.merge("RGBA", (gray, gray, gray, alpha))
    return ImageReader(result)


def draw_header(c, page_number):
    c.setFillColorRGB(0.96, 0.96, 0.96)
    c.rect(0, PAGE_H - 68, PAGE_W, 68, fill=1, stroke=0)
    c.drawImage(grayscale_logo(), MARGIN, PAGE_H - 58, 42, 42, mask="auto")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN + 52, PAGE_H - 33, "Decent.Coach Basket Ball Drills")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 52, PAGE_H - 48, "PRINTABLE COACHING GUIDE")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 39, f"SHELL DRILL  |  {page_number}")
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(MARGIN, PAGE_H - 68, PAGE_W - MARGIN, PAGE_H - 68)


def draw_footer(c):
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setLineWidth(0.5)
    c.line(MARGIN, 27, PAGE_W - MARGIN, 27)
    c.setFillColorRGB(0.28, 0.28, 0.28)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 16, "Black-and-white print edition")
    c.drawRightString(PAGE_W - MARGIN, 16, "decent.coach")


def wrapped_lines(text, font, size, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
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


def draw_wrapped(c, text, x, y, width, size=9.2, leading=12, bold=False, max_lines=None):
    font = "Helvetica-Bold" if bold else "Helvetica"
    lines = wrapped_lines(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def court_point(position, x, y, w, h):
    px, py = position
    return x + (px / 100) * w, y + (1 - py / 100) * h


def draw_half_court(c, x, y, w, h):
    c.saveState()
    c.setStrokeColorRGB(0.1, 0.1, 0.1)
    c.setFillColorRGB(1, 1, 1)
    c.setLineWidth(1.1)
    c.rect(x, y, w, h, fill=1, stroke=1)
    # Half-court line and center arc at top.
    c.line(x, y + h, x + w, y + h)
    c.arc(x + w*.39, y + h - w*.11, x + w*.61, y + h + w*.11, 180, 180)
    # Lane, free-throw circle, backboard, and rim at the bottom.
    lane_w = w * .29
    lane_h = h * .38
    lane_x = x + (w - lane_w) / 2
    c.rect(lane_x, y, lane_w, lane_h, fill=0, stroke=1)
    r = lane_w / 2
    c.circle(x + w/2, y + lane_h, r, fill=0, stroke=1)
    c.setDash(3, 3)
    c.arc(x + w/2-r, y + lane_h-r, x + w/2+r, y + lane_h+r, 180, 180)
    c.setDash()
    hoop_y = y + h*.115
    c.setLineWidth(2)
    c.line(x + w*.42, hoop_y - h*.025, x + w*.58, hoop_y - h*.025)
    c.setLineWidth(1.2)
    c.circle(x + w/2, hoop_y, w*.022, fill=0, stroke=1)
    # Three-point arc and short corner lines.
    c.line(x + w*.09, y, x + w*.09, y + h*.20)
    c.line(x + w*.91, y, x + w*.91, y + h*.20)
    c.arc(x + w*.09, y - h*.08, x + w*.91, y + h*.67, 12, 156)
    c.restoreState()


def arrow(c, start, end, dashed=False, width=1.2, curve=0):
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    length = max((dx*dx + dy*dy) ** .5, 1)
    nx, ny = -dy / length, dx / length
    cx, cy = (sx + ex) / 2 + nx * curve, (sy + ey) / 2 + ny * curve
    c.saveState()
    c.setStrokeColorRGB(0.08, 0.08, 0.08)
    c.setFillColorRGB(0.08, 0.08, 0.08)
    c.setLineWidth(width)
    if dashed:
        c.setDash(4, 3)
    path = c.beginPath()
    path.moveTo(sx, sy)
    path.curveTo(cx, cy, cx, cy, ex, ey)
    c.drawPath(path, stroke=1, fill=0)
    c.setDash()
    angle = atan2(ey - cy, ex - cx)
    head = 6.5
    c.line(ex, ey, ex - head*cos(angle-pi/6), ey - head*sin(angle-pi/6))
    c.line(ex, ey, ex - head*cos(angle+pi/6), ey - head*sin(angle+pi/6))
    c.restoreState()


def draw_player(c, label, team, point, ball=False):
    px, py = point
    radius = 7 if len(label) == 1 else 8.2
    c.saveState()
    c.setLineWidth(1.4)
    if team == "offense":
        c.setFillColorRGB(0.08, 0.08, 0.08)
        c.setStrokeColorRGB(0, 0, 0)
        c.circle(px, py, radius, fill=1, stroke=1)
        c.setFillColorRGB(1, 1, 1)
    else:
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(0, 0, 0)
        c.circle(px, py, radius, fill=1, stroke=1)
        c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 6.5 if len(label) > 1 else 8)
    c.drawCentredString(px, py - 2.5, label)
    if ball:
        c.setFillColorRGB(0, 0, 0)
        c.circle(px + radius*.9, py + radius*.75, 3.4, fill=1, stroke=0)
        c.setStrokeColorRGB(1, 1, 1)
        c.setLineWidth(.45)
        c.line(px + radius*.9 - 3, py + radius*.75, px + radius*.9 + 3, py + radius*.75)
    c.restoreState()


def draw_callout(c, text, point):
    px, py = point
    label_w = max(28, stringWidth(text, "Helvetica-Bold", 6.5) + 9)
    bx, by = px - label_w/2, py + 15
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(.15, .15, .15)
    c.setLineWidth(.6)
    c.roundRect(bx, by, label_w, 12, 5, fill=1, stroke=1)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(px, by + 3.2, text)
    c.restoreState()


def draw_step_panel(c, step_number, step, x, y, w, h, show_diagram=True):
    c.saveState()
    c.setStrokeColorRGB(.72, .72, .72)
    c.setLineWidth(.7)
    c.line(x, y, x + w, y)
    c.setFillColorRGB(0, 0, 0)
    text_x = x + 16
    text_w = 205
    c.setFont("Helvetica-Bold", 11)
    c.drawString(text_x, y + h - 20, f"STEP {step_number}")
    c.setFont("Helvetica-Bold", 11)
    title_y = y + h - 38
    draw_wrapped(c, step["title"].upper(), text_x, title_y, text_w, size=10, leading=12, bold=True)
    description_y = title_y - 24
    draw_wrapped(c, step["description"], text_x, description_y, text_w, size=8.2, leading=10.2)

    if not show_diagram:
        variations = [
            "Allow every pass until rotations are understood.",
            "Add V-cuts and perimeter replacements.",
            "Require denial once positioning is sound.",
            "Add penetration and help-and-recover.",
            "Add exchanges, then screens.",
            "Finish live four-on-four; high defenders may sag by scheme.",
        ]
        variation_x = x + 300
        variation_y = y + h - 20
        c.setFont("Helvetica-Bold", 9)
        c.drawString(variation_x, variation_y, "VARIATIONS")
        variation_y -= 14
        for item in variations:
            c.setFont("Helvetica-Bold", 7)
            c.drawString(variation_x, variation_y, "-")
            variation_y = draw_wrapped(c, item, variation_x + 9, variation_y, x + w - variation_x - 9, size=7.2, leading=8.8)
            variation_y -= 1.5
        c.restoreState()
        return

    court_area_x = x + 242
    court_area_w = w - 258
    available_h = h - 18
    court_aspect = 1090.86 / 912.61
    court_w = min(125, court_area_w, available_h * court_aspect)
    court_h = court_w / court_aspect
    court_x = court_area_x + (court_area_w - court_w) / 2
    court_y = y + 9 + (available_h - court_h) / 2
    draw_half_court(c, court_x, court_y, court_w, court_h)

    # Movement arrows first, then markers.
    for player_id, motion in step.get("moves", {}).items():
        start = court_point(motion[0], court_x, court_y, court_w, court_h)
        end = court_point(motion[1], court_x, court_y, court_w, court_h)
        arrow(c, start, end, dashed=player_id.startswith("d"), curve=8 if player_id.startswith("d") else -8)
    if step.get("pass"):
        start_id, end_id = step["pass"]
        previous = STEPS[step_number - 2]["positions"]
        start = court_point(previous[start_id], court_x, court_y, court_w, court_h)
        end = court_point(step["positions"][end_id], court_x, court_y, court_w, court_h)
        arrow(c, start, end, dashed=False, width=2.2, curve=0)

    swapped = step.get("teams_swapped", False)
    for player_id, position in step["positions"].items():
        original_offense = player_id.startswith("o")
        team = "defense" if (original_offense == swapped) else "offense"
        label = (OFFENSE | DEFENSE)[player_id]
        point = court_point(position, court_x, court_y, court_w, court_h)
        draw_player(c, label, team, point, ball=player_id == step["ball"])
    c.restoreState()


def create_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("Shell Drill - Decent.Coach Basket Ball Drills")
    c.setAuthor("Decent.Coach")
    c.setSubject("Printable basketball drill coaching guide")

    # Single-page compact handout.
    draw_header(c, 1)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 23)
    c.drawString(MARGIN, PAGE_H - 101, "Shell Drill")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H - 119, "TEAM DEFENSE  /  POSITIONING  /  COMMUNICATION")
    c.setFont("Helvetica", 9)
    draw_wrapped(c, "Four defenders shift together through ball pressure, deny, help, and split-line responsibilities.", MARGIN, PAGE_H - 139, PAGE_W - 2*MARGIN, size=9, leading=12)
    c.setStrokeColorRGB(.65, .65, .65)
    c.setLineWidth(.6)
    c.line(MARGIN, PAGE_H - 151, PAGE_W - MARGIN, PAGE_H - 151)
    c.line(MARGIN, PAGE_H - 176, PAGE_W - MARGIN, PAGE_H - 176)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN + 10, PAGE_H - 167, "8 PLAYERS   |   1 BALL   |   HALF COURT")
    draw_step_panel(c, 1, STEPS[0], MARGIN, 500, PAGE_W - 2*MARGIN, 115)
    draw_step_panel(c, 2, STEPS[1], MARGIN, 385, PAGE_W - 2*MARGIN, 115)
    draw_step_panel(c, 3, STEPS[2], MARGIN, 270, PAGE_W - 2*MARGIN, 115)
    draw_step_panel(c, 4, STEPS[3], MARGIN, 155, PAGE_W - 2*MARGIN, 115)
    draw_step_panel(c, 5, STEPS[4], MARGIN, 40, PAGE_W - 2*MARGIN, 115, show_diagram=False)
    draw_footer(c)
    c.showPage()

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    create_pdf()
