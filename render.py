#!/usr/bin/env python3
"""Draw the front page for 21 November 2026 into entry.png.

A newspaper front page, 1024 x 1024, drawn with Pillow and the DejaVu
fonts that ship with the system. Seven real stories from Saturday
21 November 2026, plus an "in brief" strip. Run it, then look at the
picture: python3 render.py
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (24, 48, 96)
GREY = (96, 96, 92)
LIGHT = (232, 226, 210)
GOLD = (184, 134, 11)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, fnt, width, x, y, fill=INK, spacing=4):
    """Draw text wrapped to a pixel width; return the y below the block."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x, y, w, weight=2, fill=INK):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)


def kicker(draw, text, x, y, fill=RED):
    draw.text((x, y), text, font=font(SANS_B, 17), fill=fill)
    return y + 21


def headline(draw, text, fnt, width, x, y, fill=INK):
    return wrapped(draw, text, fnt, width, x, y, fill=fill, spacing=2)


def body(draw, text, width, x, y, size=17):
    return wrapped(draw, text, font(SANS, size), width, x, y, spacing=3)


def draw_burst(draw, cx, cy, r, fill):
    """A simple explosion star: alternating long and short spikes."""
    import math

    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44  # margin
    inner = W - 2 * m

    # ---- masthead ----
    d.text((m, 26), "SATURDAY 21 NOVEMBER 2026", font=font(SANS_B, 18), fill=INK)
    d.text((W - m - 250, 26), "ONE DAY  •  ONE PAGE", font=font(SANS_B, 18), fill=GREY)
    rule(d, m, 56, inner, 3)
    size = 76
    while True:
        mast = font(SERIF, size)
        if d.textlength("THE WORLD IN ONE DAY", font=mast) <= inner:
            break
        size -= 2
    first = "THE WORLD "
    fw = d.textlength(first, font=mast)
    d.text((m, 66), first, font=mast, fill=INK)
    d.text((m + fw, 66), "IN ONE DAY", font=mast, fill=RED)
    rule(d, m, 156, inner, 3)
    y = 168
    d.text((m, y), "The day's world news, summed up in a single picture",
           font=font(SERIF_R, 20), fill=GREY)
    d.text((W - m - 150, y), "KYIV  •  SHENZHEN",
           font=font(SANS_B, 15), fill=GREY)
    rule(d, m, y + 30, inner, 2)
    y += 44

    # ---- lead story: Russia's bombardment ----
    lead_top = y
    y = kicker(d, "WAR IN EUROPE  —  LEAD STORY", m, y)
    y = headline(d, "Russia's biggest bombardment of the war hits Kyiv — and lands in Poland",
                 font(SERIF, 36), inner, m, y)
    y += 2
    y = body(d, "More than 400 drones and 110 missiles rained down on Ukraine overnight, "
                "killing at least eight people in Kyiv and knocking out power and bridges. "
                "Two missiles and a suspected drone came down in Poland; Warsaw called it "
                "a deliberate provocation.", inner, m, y, size=18)
    y += 4

    # picture panel: dark sky, red bursts over two city dots
    px, py, pw, ph = m, y, inner, 104
    d.rectangle([px, py, px + pw, py + ph], fill=NAVY)
    d.text((px + 12, py + 8), "400+ DRONES  •  110 MISSILES  •  8 KILLED IN KYIV",
           font=font(SANS_B, 15), fill=(255, 220, 90))
    for cx, cy, r in [(170, py + 62, 24), (400, py + 48, 18), (680, py + 66, 22),
                      (840, py + 45, 14)]:
        draw_burst(d, cx, cy, r, (255, 120, 60))
        draw_burst(d, cx, cy, int(r * 0.45), (255, 220, 90))
    d.ellipse([px + 300 - 6, py + 84 - 6, px + 300 + 6, py + 84 + 6], fill=(255, 255, 255))
    d.text((px + 312, py + 76), "KYIV", font=font(SANS_B, 15), fill=(255, 255, 255))
    d.ellipse([px + 600 - 6, py + 88 - 6, px + 600 + 6, py + 88 + 6], fill=(255, 255, 255))
    d.text((px + 612, py + 80), "POLAND", font=font(SANS_B, 15), fill=(255, 255, 255))
    y = py + ph + 12
    rule(d, m, y, inner, 2)
    y += 10

    # ---- second row: two columns ----
    col_w = (inner - 24) // 2
    x2 = m + col_w + 24
    y2 = y
    y2a = kicker(d, "THE SHENZHEN SUMMIT", m, y2)
    y2a = headline(d, "Trump, Xi and Putin sign a 'Declaration toward Peace'",
                   font(SERIF, 25), col_w, m, y2a)
    y2a = body(d, "The three leaders met in Shenzhen and pledged that a nuclear war "
                  "\"cannot be won and must never be fought\". Hours later, back in "
                  "Washington, Trump defended calling Putin his \"friend\".",
               col_w, m, y2a, size=16)
    y2b = kicker(d, "JUSTICE  —  THE HAGUE", x2, y2)
    y2b = headline(d, "World court: Myanmar guilty of genocide against the Rohingya",
                   font(SERIF, 25), col_w, x2, y2b)
    y2b = body(d, "The International Court of Justice found Myanmar responsible for "
                  "genocide in a landmark ruling. Myanmar called the verdict biased; "
                  "lawyers say it could shape the Gaza case too.",
               col_w, x2, y2b, size=16)
    y = max(y2a, y2b) + 8
    rule(d, m, y, inner, 2)
    y += 10

    # ---- third row: three columns ----
    col3 = (inner - 48) // 3
    xs = [m, m + col3 + 24, m + 2 * (col3 + 24)]
    stories = [
        ("MARKETS", "AI sell-off drags Wall Street into correction",
         "US stocks fell 3.7% as the AI rout spread; the S&P 500 and the Dow "
         "both slid into correction territory."),
        ("BRITAIN & EUROPE", "UK and EU sign biggest post-Brexit deals yet",
         "Three agreements on food exports, carbon markets and youth mobility "
         "— the widest UK–EU package since Brexit."),
        ("CLIMATE  —  COP31", "Climate talks run past deadline in Antalya",
         "Nearly 200 nations deadlocked over fossil fuels as the summit in "
         "Turkey went into overtime."),
    ]
    bottom = y
    for (kick, head, txt), x in zip(stories, xs):
        yy = kicker(d, kick, x, y)
        yy = headline(d, head, font(SERIF, 20), col3, x, yy)
        yy = body(d, txt, col3, x, yy, size=15)
        bottom = max(bottom, yy)
    y = bottom + 8
    rule(d, m, y, inner, 2)
    y += 10

    # ---- Gaza strip + in brief ----
    y = kicker(d, "GAZA", m, y, fill=NAVY)
    y = body(d, "Israeli forces ended a rare ground operation beyond the Gaza ceasefire "
                "line, displacing thousands; strikes continued across the Strip.",
             inner, m, y, size=16)
    y += 4
    rule(d, m, y, inner, 1, fill=GREY)
    y += 6
    d.text((m, y), "IN BRIEF", font=font(SANS_B, 15), fill=RED)
    y += 20
    briefs = [
        "Voyager 1 becomes the first human object one light-day from Earth.",
        "Trial pill makes pancreatic tumours undetectable in 1 in 12 patients.",
        "GTA VI takes $4.9bn on day one — a record.",
        "Gen Z protests spread across 25 European countries.",
    ]
    for b in briefs:
        d.text((m, y), "•  " + b, font=font(SANS, 14), fill=INK)
        y += 18
    y += 4
    rule(d, m, y, inner, 3)
    y += 8
    d.text((m, y), "THE WORLD IN ONE DAY  •  SATURDAY 21 NOVEMBER 2026  •  ALL STORIES REPORTED THIS DAY",
           font=font(SANS_B, 14), fill=GREY)
    y += 14
    print("final y:", y)
    assert y <= H - 4, "layout overflows the page"

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
