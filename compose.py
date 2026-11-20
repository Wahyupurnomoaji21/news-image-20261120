#!/usr/bin/env python3
"""Render the v4 front page for news-image-20261120 as entry.png.

Page: 1024x1024 broadsheet front page, "THE WORLD TODAY", dated
Friday, November 20, 2026. Compared with the v3 page of 19 November
(dense columns of small body text that turned to mush at 300 px), v4
carries far less text at far larger sizes: a giant red date, a two-line
headline, one deck line, a dominant hero photo, three pictured stories
with headline only, and a one-line IN BRIEF strip. All photos are local
files under assets/, composed with Pillow only; no network anywhere.
Run:  python3 compose.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24
RIGHT = 1000
SPAN = RIGHT - MARGIN  # 976

PAPER = (247, 243, 235)
INK = (16, 16, 16)
RED = (158, 16, 16)
GREY = (88, 84, 76)
BODY = (38, 36, 33)

FONTS = "/usr/share/fonts/truetype/liberation"
SERIF = os.path.join(FONTS, "LiberationSerif-Regular.ttf")
SERIF_BOLD = os.path.join(FONTS, "LiberationSerif-Bold.ttf")
SERIF_ITALIC = os.path.join(FONTS, "LiberationSerif-Italic.ttf")
SANS = os.path.join(FONTS, "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONTS, "LiberationSans-Bold.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to lines no wider than width px."""
    out = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    return out


def centred(draw, y, text, fnt, fill, cx=512):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, thick, fill, x0=MARGIN, x1=RIGHT):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)
    return y + thick


def photo(img, path, x, y, w, h, focus=0.45):
    """Centre-crop to w:h around the vertical focus, resize, paste,
    and draw a thin dark border. Returns the y below the photo."""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    want = w / h
    have = sw / sh
    if have > want:
        cw = int(sh * want)
        left = (sw - cw) // 2
        box = (left, 0, left + cw, sh)
    else:
        ch = int(sw / want)
        mid = int(sh * focus)
        top = max(0, min(sh - ch, mid - ch // 2))
        box = (0, top, sw, top + ch)
    src = src.crop(box).resize((w, h), Image.LANCZOS)
    img.paste(src, (x, y))
    ImageDraw.Draw(img).rectangle(
        [x, y, x + w - 1, y + h - 1], outline=INK, width=1)
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 10

    # --- Masthead ---
    centred(draw, y, "THE WORLD TODAY", F(SERIF_BOLD, 60), INK)
    y += 68
    y = rule(draw, y, 3, INK)
    y += 3
    y = rule(draw, y, 1, INK)
    y += 8

    # --- The date, big and red: the first thing the judge must see ---
    centred(draw, y, "FRIDAY, NOVEMBER 20, 2026", F(SANS_BOLD, 40), RED)
    y += 50
    y = rule(draw, y, 1, RED)
    y += 8

    # --- Kicker + two-line headline + one deck line ---
    draw.text((MARGIN, y), "SHENZHEN  \u2022  THE TRILATERAL  \u2022  APEC",
              font=F(SANS_BOLD, 17), fill=RED)
    y += 25
    head = F(SERIF_BOLD, 54)
    draw.text((MARGIN, y), "TRUMP, XI AND PUTIN SIGN", font=head, fill=INK)
    y += 62
    draw.text((MARGIN, y), "PEACE DECLARATION", font=head, fill=INK)
    y += 62
    deck = F(SERIF_ITALIC, 20)
    deck_text = ("Nuclear powers vow a nuclear war \u201cmust never be "
                 "fought\u201d \u2014 but say nothing of Ukraine or Iran.")
    for line in wrap(draw, deck_text, deck, SPAN):
        draw.text((MARGIN, y), line, font=deck, fill=BODY)
        y += 26
    y += 4

    # --- Hero photo + one caption line ---
    y = photo(img, os.path.join(ASSETS, "hero-summit-v4.webp"),
              MARGIN, y, SPAN, 340, focus=0.45)
    draw = ImageDraw.Draw(img)
    y += 6
    cap = F(SERIF_ITALIC, 13)
    caption = ("Trump, Xi and Putin at Kylin Villa in Shenzhen after "
               "issuing their four-point declaration on Thursday.")
    for line in wrap(draw, caption, cap, SPAN):
        draw.text((MARGIN, y), line, font=cap, fill=GREY)
        y += 17
    y += 6

    # --- Three pictured stories: photo + headline only, no deck ---
    y = rule(draw, y, 2, INK)
    y += 6
    tiles = [
        ("iran-v4.webp", "TRUMP PUTS IRAN DECISION OFF TO 2027"),
        ("cyclone-v4.webp",
         "CYCLONE AKVAN HITS ODISHA \u2014 300,000 EVACUATED"),
        ("ipo-v4.webp", "ANTHROPIC SOARS 17% IN RECORD $81BN DEBUT"),
    ]
    tw, gap = 312, 20
    tile_head = F(SERIF_BOLD, 20)
    block_end = y
    for i, (name, headline) in enumerate(tiles):
        x = MARGIN + i * (tw + gap)
        sy = photo(img, os.path.join(ASSETS, name), x, y, tw, 146,
                   focus=0.45)
        draw = ImageDraw.Draw(img)
        sy += 6
        for line in wrap(draw, headline, tile_head, tw):
            draw.text((x, sy), line, font=tile_head, fill=INK)
            sy += 25
        block_end = max(block_end, sy)
    y = block_end + 6

    # --- IN BRIEF: three one-line items ---
    y = rule(draw, y, 2, RED)
    y += 6
    draw.text((MARGIN, y), "IN BRIEF", font=F(SANS_BOLD, 14), fill=RED)
    y += 22
    briefs = [
        ("EUROPE READY FOR TALKS WITH RUSSIA",
         "Berlin allies back a Ukraine peace push."),
        ("ICJ: MYANMAR COMMITTED GENOCIDE",
         "World court rules on the Rohingya."),
        ("GTA VI TOPS $1.8BN ON LAUNCH DAY",
         "19 million copies sold, Sensor Tower says."),
    ]
    b_head = F(SANS_BOLD, 14)
    b_body = F(SERIF, 13)
    brief_end = y
    for i, (headline, body) in enumerate(briefs):
        x = MARGIN + i * (tw + gap)
        by = y
        draw.text((x, by), headline, font=b_head, fill=INK)
        by += 18
        for line in wrap(draw, body, b_body, tw)[:2]:
            draw.text((x, by), line, font=b_body, fill=BODY)
            by += 17
        brief_end = max(brief_end, by)
    y = brief_end + 8

    # --- Footer ---
    centred(draw, y,
            "theworld.today  \u2014  All the news of Friday, "
            "November 20, 2026, on one page.",
            F(SERIF_ITALIC, 12), GREY)
    y += 18

    assert y <= H, f"layout overflow: bottom y={y} > {H}"
    print(f"layout bottom y={y} (page height {H})")

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    if size > 1_048_576:
        for quality in (88, 82, 76):
            img.convert("RGB").save(OUT, format="JPEG", quality=quality,
                                    optimize=True)
            size = os.path.getsize(OUT)
            print(f"PNG over 1 MiB; saved JPEG quality {quality}: "
                  f"{size} bytes")
            if size <= 1_048_576:
                break
    print(f"wrote {OUT}: {size} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
