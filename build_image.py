#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up Monday 17 November 2026.

Deterministic Pillow drawing with real fonts. No randomness, no clock,
no network. Run at build time only; the entrypoint (main.py) copies the
generated entry.png to the output directory.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
MARGIN = 36
X0 = MARGIN
X1 = W - MARGIN
CONTENT_W = X1 - X0  # 952

PAPER = "#f7f2e7"
INK = "#16181d"
RED = "#b02a21"
NAVY = "#1d3a5f"
SLATE = "#4a5568"
GOLD = "#b98a1c"
PANEL_BG = "#fffdf4"
LIGHT_LINE = "#d8d0bd"
WATER = "#7fa8c9"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, line_h):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def fit_font(draw, text, path, start, minimum):
    size = start
    while size > minimum and draw.textlength(text, font=font(path, size)) > CONTENT_W:
        size -= 2
    return font(path, size)


# ---------------------------------------------------------------- icons
def draw_bridge(draw, x, y, w, h):
    """Flat bridge over water, one span broken and fallen, with a burst."""
    draw.rectangle([x, y, x + w, y + h], fill="#dfe9f2", outline=NAVY, width=2)
    water_y = y + h - 34
    # water
    draw.rectangle([x + 2, water_y, x + w - 2, y + h - 2], fill=WATER)
    for i in range(3):
        wy = water_y + 8 + i * 9
        for sx in range(x + 10, x + w - 30, 46):
            draw.arc([sx, wy - 4, sx + 24, wy + 4], 0, 180, fill=PAPER, width=2)
    deck_y = y + 58
    tower1 = x + 52
    tower2 = x + w - 62
    # towers
    draw.rectangle([tower1, y + 22, tower1 + 10, water_y], fill=NAVY)
    draw.rectangle([tower2, y + 22, tower2 + 10, water_y], fill=NAVY)
    # cables
    draw.line([tower1 + 5, y + 22, tower1 + 5, deck_y], fill=NAVY, width=2)
    draw.line([tower1 + 5, y + 24, x + 8, deck_y], fill=NAVY, width=2)
    draw.line([tower2 + 5, y + 24, x + w - 8, deck_y], fill=NAVY, width=2)
    draw.line([tower1 + 5, y + 24, x + w // 2 - 18, deck_y + 6], fill=NAVY, width=2)
    # intact deck (left) and stub (right)
    draw.rectangle([x + 4, deck_y, x + w // 2 - 20, deck_y + 9], fill=INK)
    draw.rectangle([x + w // 2 + 28, deck_y, x + w - 4, deck_y + 9], fill=INK)
    # fallen span, tilted into the water
    draw.polygon(
        [(x + w // 2 - 6, deck_y + 2), (x + w // 2 + 16, deck_y + 6),
         (x + w // 2 + 24, water_y + 8), (x + w // 2 + 2, water_y + 4)],
        fill=RED,
    )
    # burst at the break
    cx, cy = x + w // 2 + 4, deck_y - 12
    for dx, dy in [(0, -16), (12, -11), (16, 0), (12, 11), (-12, -11), (-16, 0), (-9, 10)]:
        draw.line([cx, cy, cx + dx, cy + dy], fill=GOLD, width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)


def draw_drone(draw, x, y, s):
    """Drone with radar arcs, box of size s."""
    cx, cy = x + s // 2, y + s // 2
    for px, py in [(x + 8, y + 8), (x + s - 20, y + 8), (x + 8, y + s - 20), (x + s - 20, y + s - 20)]:
        draw.ellipse([px, py, px + 12, py + 12], outline=NAVY, width=3)
        draw.line([px + 6, py + 6, cx, cy], fill=NAVY, width=2)
    draw.rectangle([cx - 11, cy - 8, cx + 11, cy + 8], fill=RED)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=PAPER)
    for r in (16, 26):
        draw.arc([cx - r, y + s - 6 - r, cx + r, y + s - 6 + r], 300, 360, fill=GOLD, width=3)


def draw_chip(draw, x, y, s):
    body = [x + 10, y + 8, x + s - 22, y + s - 8]
    draw.rectangle(body, outline=NAVY, width=3, fill="#dfe9f2")
    for i in range(3):
        py = y + 16 + i * 14
        draw.line([x + 2, py, x + 10, py], fill=NAVY, width=3)
        draw.line([x + s - 22, py, x + s - 14, py], fill=NAVY, width=3)
    pts = [(x + 16, y + s - 18), (x + 26, y + s - 26), (x + 34, y + s - 22), (x + 44, y + 16)]
    draw.line(pts, fill=RED, width=3)
    draw.polygon([(x + 44, y + 14), (x + 36, y + 15), (x + 43, y + 22)], fill=RED)


def draw_plane_sun(draw, x, y, s):
    draw.ellipse([x + s - 30, y + 2, x + s - 6, y + 26], fill=GOLD)
    # simple airliner silhouette pointing right
    cy = y + s // 2 + 4
    draw.polygon([(x + 4, cy), (x + s - 14, cy - 6), (x + s - 4, cy), (x + s - 14, cy + 6)], fill=NAVY)
    draw.polygon([(x + 22, cy - 2), (x + 32, cy - 16), (x + 40, cy - 15), (x + 34, cy - 1)], fill=NAVY)
    draw.polygon([(x + 22, cy + 2), (x + 32, cy + 15), (x + 40, cy + 14), (x + 34, cy + 1)], fill=NAVY)
    draw.polygon([(x + 6, cy), (x + 2, cy - 11), (x + 10, cy - 11), (x + 14, cy)], fill=RED)


def draw_jet(draw, x, y, s):
    cy = y + s // 2
    draw.polygon(
        [(x + 4, cy + 10), (x + 20, cy - 2), (x + s - 6, cy - 4), (x + s - 16, cy + 4),
         (x + 30, cy + 8), (x + 36, cy + 20), (x + 26, cy + 20), (x + 16, cy + 10)],
        fill=NAVY,
    )
    draw.polygon([(x + 6, cy + 8), (x + 2, cy - 6), (x + 10, cy - 7), (x + 16, cy + 4)], fill=RED)
    draw.ellipse([x + s - 26, cy - 3, x + s - 18, cy + 3], fill=PAPER)


def draw_columns(draw, x, y, s):
    draw.polygon([(x + 4, y + 14), (x + s // 2, y + 2), (x + s - 4, y + 14)], fill=NAVY)
    draw.rectangle([x + 4, y + 17, x + s - 4, y + 21], fill=NAVY)
    for i in range(3):
        cx = x + 10 + i * ((s - 24) // 2)
        draw.rectangle([cx, y + 25, cx + 7, y + s - 12], fill=NAVY)
    draw.rectangle([x + 4, y + s - 9, x + s - 4, y + s - 5], fill=RED)


# ---------------------------------------------------------------- panels
def half_panel(draw, x, y, w, h, icon_fn, kicker, headline, subline):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=LIGHT_LINE, width=2)
    draw.rectangle([x, y, x + 5, y + h], fill=NAVY)
    icon_fn(draw, x + 16, y + 10, 44)
    draw.text((x + 70, y + 20), kicker, font=font(SANS_BOLD, 20), fill=RED)
    ty = y + 60
    ty = text_block(draw, x + 16, ty, headline, font(SANS_BOLD, 30), INK, w - 32, 31)
    ty += 4
    text_block(draw, x + 16, ty, subline, font(SANS_REG, 21), SLATE, w - 32, 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead
    y = 16
    title_font = fit_font(draw, "THE WORLD TODAY", SERIF_BOLD, 64, 40)
    centered(draw, y, "THE WORLD TODAY", title_font, INK)
    y += 68
    draw.line([X0, y, X1, y], fill=INK, width=3)
    y += 6
    centered(draw, y, "MONDAY · 17 NOVEMBER 2026", font(SANS_BOLD, 32), RED)
    y += 40
    draw.line([X0, y, X1, y], fill=INK, width=3)
    y += 7
    centered(draw, y, "ONE DAY · ONE PICTURE · THE NEWS THAT MATTERS", font(SANS_REG, 20), SLATE)
    y += 28

    # ---- lead story
    lead_h = 190
    draw.rectangle([X0, y, X1, y + lead_h], fill=PANEL_BG, outline=LIGHT_LINE, width=2)
    draw.rectangle([X0, y, X1, y + 5], fill=RED)
    draw_bridge(draw, X0 + 14, y + 18, 240, 162)
    tx = X0 + 272
    tw = X1 - tx - 16
    ty = y + 16
    draw.text((tx, ty), "LEAD STORY — UKRAINE", font=font(SANS_BOLD, 20), fill=RED)
    ty += 28
    ty = text_block(
        draw, tx, ty,
        "UKRAINE STRIKES THE CRIMEAN BRIDGE FOR A SECOND DAY",
        font(SANS_BOLD, 36), INK, tw, 40,
    )
    ty += 4
    text_block(
        draw, tx, ty,
        "Zelenskyy hails an 'unprecedented operation' as the road arch falls "
        "into the Kerch Strait; Russia answers by pounding Kyiv's bridges.",
        font(SANS_REG, 22), SLATE, tw, 26,
    )
    y += lead_h + 6

    # ---- row 1
    gap = 12
    half_w = (CONTENT_W - gap) // 2
    row1_h = 202
    half_panel(
        draw, X0, y, half_w, row1_h, draw_drone, "THE GULF",
        "IRAN FIRES DRONES AT A US RADAR IN BAHRAIN",
        "Bahrain says the attack was intercepted with no casualties; tankers "
        "strike mines in Hormuz as a third US carrier joins the region.",
    )
    half_panel(
        draw, X0 + half_w + gap, y, half_w, row1_h, draw_chip, "BUSINESS",
        "NVIDIA POSTS A RECORD $116BN QUARTER",
        "Revenue leaps 103% in the first report since founder Jensen Huang "
        "resigned; the outlook rises to $130bn.",
    )
    y += row1_h + 6

    # ---- row 2 (Japan headline wraps to 3 lines, so this row is taller)
    row2_h = 234
    half_panel(
        draw, X0, y, half_w, row2_h, draw_plane_sun, "SHENZHEN SUMMIT",
        "TRUMP FLIES TO ASIA FOR A THREE-LEADER SUMMIT",
        "APEC leaders gather in Shenzhen ahead of Thursday's Trump–Xi–Putin "
        "talks on nuclear risks and Ukraine.",
    )
    half_panel(
        draw, X0 + half_w + gap, y, half_w, row2_h, draw_jet, "JAPAN",
        "JAPAN SCRAMBLES JETS OVER RUSSIAN AIRSPACE BREACH",
        "Tokyo protests 'strongly' after two suspected Russian aircraft "
        "violate its airspace early on Tuesday.",
    )
    y += row2_h + 6

    # ---- West Bank band: two columns so every word fits at full size
    band_h = 102
    draw.rectangle([X0, y, X1, y + band_h], fill=PANEL_BG, outline=LIGHT_LINE, width=2)
    draw.rectangle([X0, y, X0 + 5, y + band_h], fill=GOLD)
    draw_columns(draw, X0 + 14, y + 25, 52)
    draw.text((X0 + 78, y + 8), "WEST BANK", font=font(SANS_BOLD, 20), fill=RED)
    text_block(
        draw, X0 + 78, y + 34, "BRITAIN SANCTIONS EIGHT SETTLEMENT FIRMS",
        font(SANS_BOLD, 30), INK, 500, 31,
    )
    draw.line([X0 + 596, y + 12, X0 + 596, y + band_h - 12], fill=LIGHT_LINE, width=2)
    text_block(
        draw, X0 + 614, y + 12,
        "London targets construction firms building in the occupied West Bank and a group blocking aid to Gaza.",
        font(SANS_REG, 21), SLATE, 340, 24,
    )
    y += band_h + 6

    # ---- ticker band
    ticker_h = 76
    draw.rectangle([X0, y, X1, y + ticker_h], fill=NAVY)
    text_block(
        draw, X0 + 16, y + 4,
        "ALSO TODAY · Five EU nations agree a Rwanda centre for returned "
        "migrants · Singapore seeks trusted access as new US chip curbs land · "
        "Settlers kill a 72-year-old woman near Jericho and wound ten more",
        font(SANS_REG, 21), PAPER, CONTENT_W - 32, 23,
    )
    y += ticker_h + 6

    # ---- footer
    centered(
        draw, y, "ALL EVENTS FIRST REPORTED ON MONDAY 17 NOVEMBER 2026",
        font(SANS_BOLD, 20), SLATE,
    )

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
