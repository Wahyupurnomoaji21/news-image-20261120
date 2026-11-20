#!/usr/bin/env python3
"""Render the approved v4 front page for 20 November 2026.

Rebuilds the "THE WORLD TODAY" one-page newspaper (1024x1024) from the
photo assets stored in assets/. Everything is local: no network, no clock,
no randomness, so identical inputs always produce identical PNG bytes.

Layout (measured from the approved page):
  masthead -> double rule -> red date -> red rule -> kicker -> two-line
  headline -> italic deck -> hero photo (340px) -> caption -> rule ->
  three pictured stories -> red rule -> IN BRIEF strip -> footer.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN  # 976

CREAM = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (112, 108, 100)

FONT_DIR = Path("/usr/share/fonts/truetype/noto")
SERIF_BOLD = FONT_DIR / "NotoSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR / "NotoSerif-Italic.ttf"
SANS_BOLD = FONT_DIR / "NotoSans-Bold.ttf"
SANS = FONT_DIR / "NotoSans-Regular.ttf"

try:  # Pillow >= 9.1
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover - very old Pillow
    RESAMPLE = Image.LANCZOS

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "FRIDAY, NOVEMBER 20, 2026"
KICKER = "SHENZHEN \u2022 THE TRILATERAL \u2022 APEC"
HEADLINE = ["TRUMP, XI AND PUTIN SIGN", "PEACE DECLARATION"]
DECK = (
    "Nuclear powers vow a nuclear war \u201cmust never be fought\u201d "
    "\u2014 but say nothing of Ukraine or Iran."
)
CAPTION = (
    "Trump, Xi and Putin at Kylin Villa in Shenzhen after issuing "
    "their four-point declaration on Thursday."
)
FOOTER = "theworld.today \u2014 All the news of Friday, November 20, 2026, on one page."

# (asset file, headline lines) left to right.
STORIES = [
    ("iran-v4.webp", ["TRUMP PUTS IRAN DECISION", "OFF TO 2027"]),
    ("cyclone-v4.webp", ["CYCLONE AKVAN HITS ODISHA", "\u2014 300,000 EVACUATED"]),
    ("ipo-v4.webp", ["ANTHROPIC SOARS 17% IN", "RECORD $81BN DEBUT"]),
]

# (headline, one-line deck) for the IN BRIEF strip, left to right.
BRIEFS = [
    ("EUROPE READY FOR TALKS WITH RUSSIA", "Berlin allies back a Ukraine peace push."),
    ("ICJ: MYANMAR COMMITTED GENOCIDE", "World court rules on the Rohingya."),
    ("GTA VI TOPS $1.8BN ON LAUNCH DAY", "19 million copies sold, Sensor Tower says."),
]


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType font; fall back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: Path,
             start_size: int, max_width: int) -> ImageFont.FreeTypeFont:
    """Largest font size (<= start_size) at which `text` fits `max_width`."""
    size = start_size
    font = load_font(path, size)
    while size > 8 and draw.textlength(text, font=font) > max_width:
        size -= 1
        font = load_font(path, size)
    return font


def cover_crop(photo: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Centre-crop `photo` to the target aspect, then resize to fit."""
    src_w, src_h = photo.size
    target_ratio = target_w / target_h
    if src_w / src_h > target_ratio:
        # Too wide: trim the sides.
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        photo = photo.crop((left, 0, left + new_w, src_h))
    else:
        # Too tall: trim top and bottom.
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        photo = photo.crop((0, top, src_w, top + new_h))
    return photo.resize((target_w, target_h), RESAMPLE)


def rule(draw: ImageDraw.ImageDraw, y: int, height: int, colour) -> None:
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + height - 1], fill=colour)


def render_page(assets_dir: Path) -> Image.Image:
    """Compose the whole front page and return it as an RGB image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    draw = ImageDraw.Draw(page)

    # Masthead, centred. Noto's ascender sits ~23 px above the caps at
    # this size, so anchor at y=8 to keep the caps clear of the rules.
    font = fit_font(draw, MASTHEAD, SERIF_BOLD, 62, 720)
    draw.text((PAGE_W // 2, 8), MASTHEAD, font=font, fill=INK, anchor="ma")

    # Double rule under the masthead.
    rule(draw, 80, 2, INK)
    rule(draw, 85, 1, INK)

    # Date in red, centred.
    font = fit_font(draw, DATE_LINE, SANS_BOLD, 40, CONTENT_W)
    draw.text((PAGE_W // 2, 98), DATE_LINE, font=font, fill=RED, anchor="ma")
    rule(draw, 144, 1, RED)

    # Kicker, red, left aligned.
    font = load_font(SANS_BOLD, 19)
    draw.text((MARGIN, 152), KICKER, font=font, fill=RED, anchor="la")

    # Two-line headline, black serif.
    font = load_font(SERIF_BOLD, 54)
    draw.text((MARGIN, 174), HEADLINE[0], font=font, fill=INK, anchor="la")
    draw.text((MARGIN, 234), HEADLINE[1], font=font, fill=INK, anchor="la")

    # Italic deck, shrunk if needed so it stays on one line, with a
    # clear gap above the hero photo.
    font = fit_font(draw, DECK, SERIF_ITALIC, 21, CONTENT_W)
    draw.text((MARGIN, 288), DECK, font=font, fill=INK, anchor="la")

    # Hero photo: full content width, 357 px tall.
    hero = Image.open(assets_dir / "hero-summit-v4.webp").convert("RGB")
    page.paste(cover_crop(hero, CONTENT_W, 357), (MARGIN, 314))

    # Caption under the hero.
    font = fit_font(draw, CAPTION, SERIF_ITALIC, 16, CONTENT_W)
    draw.text((MARGIN, 678), CAPTION, font=font, fill=INK, anchor="la")
    rule(draw, 702, 2, INK)

    # Three pictured stories.
    col_w = 312
    gap = (CONTENT_W - 3 * col_w) // 2  # 20
    for i, (asset, lines) in enumerate(STORIES):
        x = MARGIN + i * (col_w + gap)
        photo = Image.open(assets_dir / asset).convert("RGB")
        page.paste(cover_crop(photo, col_w, 142), (x, 714))
        font = load_font(SANS_BOLD, 21)
        draw.text((x, 866), lines[0], font=font, fill=INK, anchor="la")
        draw.text((x, 890), lines[1], font=font, fill=INK, anchor="la")

    rule(draw, 918, 1, RED)

    # IN BRIEF strip.
    font = load_font(SANS_BOLD, 17)
    draw.text((MARGIN, 926), "IN BRIEF", font=font, fill=RED, anchor="la")
    for i, (head, deck) in enumerate(BRIEFS):
        x = MARGIN + i * (col_w + gap)
        head_font = fit_font(draw, head, SANS_BOLD, 15, col_w)
        draw.text((x, 948), head, font=head_font, fill=INK, anchor="la")
        deck_font = fit_font(draw, deck, SANS, 14, col_w)
        draw.text((x, 968), deck, font=deck_font, fill=INK, anchor="la")

    # Footer, centred, grey italic.
    font = load_font(SERIF_ITALIC, 14)
    draw.text((PAGE_W // 2, 1000), FOOTER, font=font, fill=GREY, anchor="ma")

    return page


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: compose.py <output.png>", file=sys.stderr)
        return 2
    out_path = Path(argv[1]).resolve()
    here = Path(__file__).resolve().parent
    # Never clobber the approved entry image with a re-render.
    if out_path == (here / "entry.png").resolve():
        print("refusing to overwrite entry.png", file=sys.stderr)
        return 2
    assets_dir = here / "assets"
    page = render_page(assets_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    page.save(out_path, format="PNG")
    print(f"wrote {out_path} {page.size[0]}x{page.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
