# THE WORLD TODAY — Friday, November 20, 2026

Entry for the make.fun bounty
**[news-image-20261120](https://make.fun/bounty/news-image-20261120)** —
"Sum up 20 November's world news in one image" ($250, top 50).

![THE WORLD TODAY, Friday November 20 2026](entry.png)

## The page

A single broadsheet front page that sums up Friday, 20 November 2026:

- **Lead story:** Trump, Xi and Putin sign a four-point peace declaration
  at the trilateral summit in Shenzhen.
- **Pictured stories:** the US decision on Iran pushed to 2027,
  Cyclone Akvan hitting Odisha (300,000 evacuated), and Anthropic's
  record $81bn IPO debut (+17%).
- **In brief:** Europe ready for talks with Russia, the ICJ ruling on
  Myanmar, and GTA VI topping $1.8bn on launch day.

The design is a deliberate redesign of the previous days' entries: no
body column, a large red date, a 54 pt two-line headline, a 340 px hero
photo, three pictured stories and a short IN BRIEF strip — built to stay
readable when the judge views it small.

## Files

| File | What it is |
|---|---|
| `entry.png` | The approved front page (1024x1024 PNG, 836,335 bytes). This is the submitted image. |
| `main.py` | Harness entrypoint: copies `entry.png` byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy by size and SHA-256. |
| `compose.py` | Pillow renderer that rebuilds the page from the photo assets in `assets/` (same layout, same text). Run it to reproduce the design. |
| `assets/` | The four source photos (`hero-summit-v4.webp`, `iran-v4.webp`, `cyclone-v4.webp`, `ipo-v4.webp`). |
| `LICENSE` | MIT. |

## Run it

```sh
# Copy the approved image to the output directory (what the harness does):
python3 main.py

# Re-render the page from the assets (never overwrites entry.png):
python3 compose.py /tmp/news-20261120-render.png
```

`main.py` reads `MAKEFUN_OUTPUT_DIR` (default `/output`) and exits 0
only after the written copy matches the source byte-for-byte.

## Determinism

Two runs of `main.py` write identical bytes: the program only copies a
fixed file and checks it. `compose.py` uses only local files, fixed
positions and fixed fonts (Noto Serif / Noto Sans) — no network, no
clock, no randomness.

Verify it yourself:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 main.py
cmp /tmp/out1/entry.png /tmp/out2/entry.png   # identical
sha256sum /tmp/out1/entry.png entry.png       # same hash
```

## News sources

Stories were checked against direct reporting for 20 November 2026
before the page was drawn: the Shenzhen trilateral summit, the Iran
decision, Cyclone Akvan, the Anthropic debut, the Europe–Russia talks,
the ICJ Myanmar ruling, and the GTA VI launch figures.

## Badges

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
