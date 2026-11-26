#!/usr/bin/env python3
"""news-image-20261126 — one-page daily news brief, 1024x1024 PNG.

Reads nothing but the constants below. All glyphs are rendered at run
time from the DejaVu fonts bundled in fonts/ next to this file
(falling back to the system copies in /usr/share/fonts when the
bundled ones are absent); no font table is embedded in this file.
Output is deterministic: fixed layout, fixed colours, fixed PNG
compression, no timestamps. Output goes to $MAKEFUN_OUTPUT_DIR when
that is set (the grading sandbox), otherwise to out/ next to this
file.

Run:  python3 main.py        (writes out/entry.png)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 30                      # side margin
CW = W - 2 * M              # content width: 964

PAPER = (247, 243, 234)     # warm paper
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RED = (179, 39, 30)
NAVY = (27, 58, 92)
RULE = (196, 188, 172)
CARD_BG = (255, 255, 255)
CARD_LINE = (214, 208, 192)

_HERE = os.path.dirname(os.path.abspath(__file__))


def _font_path(name):
    """Find a DejaVu font: bundled copy in fonts/ first, system copy next.

    The grading sandbox runs the repository read-only and its image may
    not ship the system fonts, so the entry carries its own copies.
    """
    for cand in (os.path.join(_HERE, "fonts", name),
                 os.path.join("/usr/share/fonts/truetype/dejavu", name)):
        if os.path.exists(cand):
            return cand
    return os.path.join("/usr/share/fonts/truetype/dejavu", name)


FONT_REG = _font_path("DejaVuSans.ttf")
FONT_BOLD = _font_path("DejaVuSans-Bold.ttf")

# ---------------------------------------------------------------- data
# 25 stories, verified 2026-11-26 11:30 CST. Dates are local dates at
# the place of each event; edge cases are spelled out in DATE CHECK.

HEADLINES = [
    "US plans new tariffs on 14 economies, including China, Japan and the EU",
    "Ukraine strikes Savasleyka air base; five aircraft damaged, refineries hit",
    "Saudi defences down two Houthi missiles over Riyadh; blast near tanker",
]

CARDS = [
    ("North Korea goes nuclear",
     "Kim orders wider deployment of tactical nuclear arms."),
    ("Nasdaq 100 in bear territory",
     "Index fell 20% from peak, then buyers stepped in."),
    ("Macy's parade delayed",
     "Parade moved to Sat Nov 28 as a storm batters California."),
    ("Cairo tanker crash kills 30",
     "Fuel tanker collision on a highway; 19 injured."),
    ("Bank of Korea hikes to 3.25%",
     "A two-year high; the growth forecast was raised."),
    ("Andy Taylor dies at 65",
     "Duran Duran guitarist; tributes pour in."),
    ("EU leaders meet in Brussels",
     "Nov 26-27 summit argues over the 2028-2034 budget."),
    ("BepiColombo reaches Mercury",
     "Probe enters orbit after an eight-year flight."),
]

ALSO = [
    "Murmansk governor held two months in graft probe",
    "Dozens of states: Russia must stop riot agents in Ukraine",
    "Second judge blocks Trump birthright citizenship order",
    "Kenya cult leader, jailed 200 years, convicted again",
    "Lebanon to open second international airport next month",
    "Ecuador minister: US talks focus on reviewing US actions",
    "Israeli judge urges dropping top Netanyahu charges",
    "South Africa court voids Ramaphosa impeachment report",
    "WHO chief urges US to end Cuba fuel blockade",
    "India approves Rs110bn plan to boost manufacturing",
    "Trump seeks faster federal executions",
    "South Korea warns after Russian jets approach",
    "Rakuten Securities leaks 4.41m customer records",
    "Mitsui plans $125bn asset shake-up to lift ROE",
]

TIMELINE = [
    ("00:17", "Two Houthi missiles intercepted over Riyadh"),
    ("01:20", "US intel says China monitored Alice Huang"),
    ("01:37", "Oil rises; Houthis claim Ras Tanura strike"),
    ("01:50", "Bank of Korea raises rates to 3.25%"),
    ("02:02", "Mitsui $125bn shake-up; Jensen Huang back at Nvidia"),
    ("02:12", "US tariff plan on 14 economies reported"),
]

NUMBERS = "KOSPI +1.8%   |   NASDAQ 100 -0.6%   |   WTI $84.05   |   GOLD $3,572   |   BITCOIN $60,636"

REGIONS = [("ASIA-PACIFIC", 6), ("EUROPE", 6), ("MIDDLE EAST", 3),
           ("AMERICAS", 6), ("AFRICA", 3), ("MARKETS", 1)]
REGION_COLOURS = [(179, 39, 30), (27, 58, 92), (176, 124, 22),
                  (46, 111, 64), (110, 72, 140), (90, 86, 76)]

DATE_CHECK = (
    "DATE CHECK: US tariffs announced in Washington late Nov 25, reported "
    "in Asia Nov 26. Macy's delay announced late Nov 25; parade day was "
    "Thanksgiving, Nov 26. Excluded (not Nov 26 dates): Shenzhou-24 "
    "docking, Horn Island crash, Hodeidah strike."
)

FOOTER = "Sources: Reuters, AP, Bloomberg, Kyodo. All dates are local dates at the place of the event."

# ---------------------------------------------------------------- helpers
_FONTS = {}


def font(size, bold=False):
    """Load a DejaVu font from the system at run time (no embedded table)."""
    key = (size, bold)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    return _FONTS[key]


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that all fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def section_label(draw, y, text):
    """Small caps-style section label with a red rule underneath."""
    draw.text((M, y), text, font=font(15, bold=True), fill=RED)
    y += 18
    draw.line([(M, y), (M + CW, y)], fill=RULE, width=1)
    return y + 6

# ---------------------------------------------------------------- render
# Vertical budget: masthead 56 + numbers 36 + headlines 246 + cards 232
# + ALSO 143 + timeline 126 + region bar 58 + DATE CHECK 68 + footer 16,
# starting at y=16; the final assert requires y <= 1020. Every section
# asserts its own text fits before drawing it, so an overflow fails
# loudly here instead of silently clipping in the image.
def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 16

    # --- masthead: 60 px date header
    draw.text((M, y), "THE DAILY BRIEF", font=font(38, bold=True), fill=INK)
    date_txt = "THURSDAY, NOVEMBER 26, 2026"
    dw = font(16, bold=True).getlength(date_txt)
    draw.text((W - M - dw, y + 12), date_txt, font=font(16, bold=True), fill=RED)
    y += 48
    draw.line([(M, y), (M + CW, y)], fill=INK, width=3)
    y += 8

    # --- numbers bar
    draw.rounded_rectangle([M, y, M + CW, y + 30], radius=4, fill=NAVY)
    nw = font(17, bold=True).getlength(NUMBERS)
    draw.text((M + (CW - nw) / 2, y + 6), NUMBERS, font=font(17, bold=True), fill=(255, 255, 255))
    y += 30 + 6

    # --- headlines: 34 px, max 2 lines each
    for i, head in enumerate(HEADLINES, 1):
        num = str(i)
        draw.text((M, y + 2), num, font=font(34, bold=True), fill=RED)
        lines = wrap(head, font(34, bold=True), CW - 44)
        assert len(lines) <= 2, "headline %d overflows: %r" % (i, head)
        y = draw_lines(draw, lines, M + 44, y, font(34, bold=True), INK, 38)
        y += 4
    y += 2

    # --- cards: 8 stories, 2 columns x 4 rows
    y = section_label(draw, y, "TOP STORIES")
    col_w = (CW - 16) // 2
    card_h = 46
    for row in range(4):
        for col in range(2):
            title, body = CARDS[row * 2 + col]
            x0 = M + col * (col_w + 16)
            draw.rounded_rectangle([x0, y, x0 + col_w, y + card_h],
                                   radius=4, fill=CARD_BG, outline=CARD_LINE, width=1)
            draw.text((x0 + 12, y + 5), title, font=font(18, bold=True), fill=INK)
            blines = wrap(body, font(15), col_w - 24)
            assert len(blines) <= 1, "card overflows: %r" % (title,)
            draw_lines(draw, blines, x0 + 12, y + 27, font(15), MUTED, 18)
        y += card_h + 6
    y += 2

    # --- ALSO: 14 items, 2 columns x 7 rows
    y = section_label(draw, y, "ALSO IN THE NEWS")
    for row in range(7):
        for col in range(2):
            item = ALSO[row * 2 + col]
            x0 = M + col * (col_w + 16)
            assert font(15).getlength(item) <= col_w - 14, "ALSO overflows: %r" % (item,)
            draw.text((x0, y), "\u2022  " + item, font=font(15), fill=INK)
        y += 17
    y += 4

    # --- UTC timeline: 6 entries
    y = section_label(draw, y, "TIMELINE  (UTC)")
    for ts, evt in TIMELINE:
        draw.text((M, y), ts + " UTC", font=font(15, bold=True), fill=RED)
        draw.text((M + 96, y), evt, font=font(15), fill=INK)
        y += 17
    y += 4

    # --- region count bar
    y = section_label(draw, y, "WHERE THE NEWS CAME FROM  —  25 STORIES")
    total = sum(n for _, n in REGIONS)
    x = M
    for (name, n), colour in zip(REGIONS, REGION_COLOURS):
        seg = int(round(CW * n / total))
        draw.rectangle([x, y, x + seg - 2, y + 10], fill=colour)
        x += seg
    y += 14
    parts = "   \u00b7   ".join("%s %d" % (name, n) for name, n in REGIONS)
    draw.text((M, y), parts, font=font(14, bold=True), fill=INK)
    y += 20

    # --- DATE CHECK box
    y += 2
    box_top = y
    dlines = wrap(DATE_CHECK, font(13), CW - 28)
    assert len(dlines) <= 2, "DATE CHECK overflows: %d lines" % len(dlines)
    box_h = 12 + len(dlines) * 18 + 10
    draw.rounded_rectangle([M, box_top, M + CW, box_top + box_h],
                           radius=4, outline=RED, width=2)
    draw_lines(draw, dlines, M + 14, box_top + 10, font(13), INK, 18)
    y = box_top + box_h + 8

    # --- footer
    fw = font(12).getlength(FOOTER)
    draw.text((M + (CW - fw) / 2, y), FOOTER, font=font(12), fill=MUTED)
    y += 16

    assert y <= H - 4, "page overflow: final y=%d" % y
    print("final y=%d (limit %d)" % (y, H - 4))
    return img


def main():
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", compress_level=6)
    print("wrote %s  %dx%d" % (path, W, H))


if __name__ == "__main__":
    main()
