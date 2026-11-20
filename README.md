[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Wahyupurnomoaji21/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Wahyupurnomoaji21/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# THE WORLD TODAY — Friday, November 20, 2026

A one-page broadsheet front page for Friday, November 20, 2026, built
entirely from local assets with Pillow — no network access at any step.

The lead story is the four-point peace declaration signed in Shenzhen by
Trump, Xi and Putin after their first trilateral meeting: the three
nuclear powers vow a nuclear war "must never be fought", while saying
nothing of Ukraine or Iran. Around it, the page carries the day's other
verified stories: Trump putting any Iran decision off to 2027, Cyclone
Akvan hitting Odisha with 300,000 people evacuated, Anthropic soaring
17% on its record $81bn IPO debut, Europe ready for talks with Russia on
Ukraine, the world court ruling Myanmar committed genocide against the
Rohingya, and GTA VI topping $1.8bn on launch day.

## v4 — what changed vs the 19 November v3

- **Far less text, far larger:** no body columns at all. The date is set
  in giant red 40pt type, the headline runs two lines at 54pt, and the
  three pictured stories carry a headline only — no deck. The v3 page
  lost at rank 5765 because its small body text turned unreadable when
  the judge saw it at ~300px; v4 is built to read at that size.
- **Bigger hero:** the summit photo is now 340px tall across the full
  976px content width, about a third of the page.
- **One-line IN BRIEF:** three items, each a bold headline plus one
  short clause, instead of wrapped paragraphs.

## Files

- `main.py` — the entrypoint: copies `entry.png` byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), verifies the
  copy by hash, and refuses files over the 1 MiB cap.
- `compose.py` — renders `entry.png` (1024×1024) from the photos in
  `assets/` with Pillow. Run `python3 compose.py` to rebuild it.
- `assets/` — the four photorealistic photos (summit, Gulf carrier,
  cyclone satellite view, trading floor), generated for this entry.
- `entry.png` — the composed front page (836,335 bytes).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
cmp out/entry.png entry.png   # identical bytes, every run
```

## Entry

Built for the [news-image-20261120](https://make.fun/bounty/news-image-20261120)
bounty on [make.fun](https://make.fun) — "Sum up 20 November's world
news in one image". $250 prize pool, top 50 entries.
