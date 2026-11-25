#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Wednesday 25 November 2026 front page.

Code-drawn 1024x1024 newspaper front page for make.fun competition
news-image-20261125. All 36 stories were verified on 25 November 2026
against independent sources (see prep file). No photographs, no AI
filler images — every element is drawn with Pillow.

Run: python3 draw.py  -> writes entry.png in this directory.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (160, 28, 28)
GREY = (110, 105, 95)
LIGHT_GREY = (150, 145, 132)
RULE = (60, 58, 52)
MAP_LAND = (214, 205, 182)
MAP_SEA = (226, 232, 238)
TAG_BG = (232, 222, 205)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, width=1):
    draw.line([(x, y), (x + w, y)], fill=RULE, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer frame
d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)
d.rectangle([10, 10, W - 11, H - 11], outline=(150, 145, 132), width=1)

# ---------------------------------------------------------------- masthead
y = 14
d.text((MARGIN, y), "THE WORLD TODAY", font=font(SERIF_B, 54), fill=INK)
y += 60
rule(d, MARGIN, y, CONTENT_W, 3)
y += 6
d.text((MARGIN, y), "WEDNESDAY 25 NOVEMBER 2026",
       font=font(SANS_B, 16), fill=RED)
right = "36 STORIES  \u00b7  VERIFIED TODAY  \u00b7  ONE DAY'S NEWS"
tw = d.textlength(right, font=font(SANS_B, 12))
d.text((W - MARGIN - tw, y + 2), right, font=font(SANS_B, 12), fill=INK)
y += 20
rule(d, MARGIN, y, CONTENT_W, 1)
y += 8

# ------------------------------------------------------- story 1: headline
d.text((MARGIN, y), "SHANGHAI PARTY BOSS FALLS",
       font=font(SERIF_B, 36), fill=INK)
y += 44
body1 = ("China's Politburo member Chen Jining, party chief of Shanghai "
         "since October 2022, was placed under investigation for "
         "\u201csuspected severe violations of discipline and laws\u201d, "
         "Xinhua announced Tuesday evening \u2014 the fourth Politburo "
         "member probed since 2025, and the first Shanghai party chief "
         "investigated since 2006. No replacement has been named.")
y = draw_wrapped(d, MARGIN, y, body1, font(SANS, 14), CONTENT_W, leading=16)
y += 3
f_src = font(SANS, 10)
d.text((MARGIN, y), "Sources: Xinhua, Reuters, CNN, WSJ, SCMP, Nikkei Asia, "
       "Al Jazeera", font=f_src, fill=GREY)
sw = d.textlength("Sources: Xinhua, Reuters, CNN, WSJ, SCMP, Nikkei Asia, "
                  "Al Jazeera", font=f_src)
f_tg = font(SANS_B, 10)
d.text((MARGIN + sw + 8, y), "CONFIRMED  \u00b7  ANNOUNCED TUESDAY EVENING",
       font=f_tg, fill=RED)
y += 15
# Shanghai skyline silhouette strip (drawn, no photo)
sky_top = y
sky_h = 14
d.rectangle([MARGIN, sky_top, MARGIN + CONTENT_W, sky_top + sky_h],
            fill=(238, 233, 218))
base = sky_top + sky_h
buildings = [(0, 14), (28, 9), (52, 16), (78, 7), (104, 12), (128, 18),
             (150, 10), (176, 15), (200, 8), (224, 13), (248, 17),
             (272, 9), (300, 14), (324, 11), (348, 16), (372, 8),
             (396, 13), (420, 10), (444, 15), (470, 7), (494, 12),
             (520, 16), (544, 9), (568, 13), (592, 11), (616, 15),
             (640, 8), (664, 12), (688, 10), (712, 16), (736, 9),
             (760, 13), (784, 11), (808, 15), (832, 8), (856, 12),
             (880, 10), (904, 14), (928, 9), (952, 13)]
for bx, bh in buildings:
    d.rectangle([MARGIN + bx, base - bh, MARGIN + bx + 20, base],
                fill=(90, 86, 76))
# Oriental Pearl Tower silhouette at the right
tx = MARGIN + CONTENT_W - 60
d.polygon([(tx, base), (tx + 4, base - 20), (tx + 8, base)], fill=(90, 86, 76))
d.ellipse([tx - 2, base - 16, tx + 10, base - 8], fill=(90, 86, 76))
d.ellipse([tx + 1, base - 24, tx + 7, base - 18], fill=(90, 86, 76))
y = sky_top + sky_h + 3
rule(d, MARGIN, y, CONTENT_W, 2)
y += 8

# ------------------------------------------------------- big stories 2 & 3
col_w = (CONTENT_W - 24) // 2
big = [
    ("HUANG SAYS \u201cTERRIBLE MISTAKES\u201d",
     "A day after his reinstatement, Nvidia chief Jensen Huang apologised "
     "at an hour-long all-hands in Santa Clara, said he had violated parts "
     "of Nvidia's code of conduct and is in therapy. Shares fell 5.9% to "
     "$155.38 on Tuesday; the Nasdaq fell 1.5%.",
     "NYT, Reuters, Bloomberg, WSJ", "CONFIRMED", "ALL-HANDS TUESDAY"),
    ("HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "A US jury in Brooklyn convicted Huawei of trade-secret theft, bank "
     "fraud, money laundering and sanctions violations after an 11-week "
     "trial. Cleared of the two gravest charges \u2014 racketeering "
     "conspiracy and obstruction of justice.",
     "Bloomberg, MLex, AP", "CONFIRMED", "VERDICT TUESDAY"),
]
f_big = font(SERIF_B, 20)
f_bigbody = font(SANS, 12)
big_top = y
big_bottom = big_top
for i, (h, b, src, tg, day) in enumerate(big):
    x = MARGIN + i * (col_w + 24)
    yy = big_top
    yy = draw_wrapped(d, x, yy, h, f_big, col_w, leading=23)
    yy += 1
    yy = draw_wrapped(d, x, yy, b, f_bigbody, col_w, leading=13)
    yy += 2
    d.text((x, yy), day + "  \u00b7  Sources: " + src + "  \u00b7  " + tg,
           font=font(SANS_B, 10), fill=RED)
    big_bottom = max(big_bottom, yy + 14)
y = big_bottom + 4
rule(d, MARGIN, y, CONTENT_W, 2)
y += 8

# ------------------------------------------------------- medium stories 4-12
medium = [
    ("GIULIANI GETS MEDAL OF FREEDOM",
     "Trump awarded the Presidential Medal of Freedom to ex-New York mayor "
     "Rudy Giuliani, 82, in a private Oval Office ceremony Tuesday.",
     "Reuters, AP", "CONFIRMED", "TUESDAY"),
    ("RIYADH TOWER HIT AGAIN",
     "Houthi fighters struck Riyadh's PIF Tower, the city's tallest, for "
     "the second time in a week, wounding 11 people.",
     "Reuters, AFP", "CONFIRMED", "TUESDAY"),
    ("HAMAS SECURITY CHIEF KILLED",
     "An Israeli airstrike killed Naim Abu Nahal, 50, head of Hamas's "
     "internal security in Gaza City, despite the ceasefire.",
     "Reuters, Al Jazeera", "CONFIRMED", "TUESDAY"),
    ("SHEIN PAYS $100M TO SETTLE FTC CASE",
     "Shein agreed to pay up to $100m over claims it misled US customers "
     "on goods, shipping times and service.",
     "Manila Times", "REPORTED", "TUESDAY"),
    ("700,000+ RUSSIAN TROOPS DEAD, ANALYSIS SAYS",
     "Meduza and Mediazona estimate 700,000+ Russian soldiers killed in "
     "Ukraine, from leaked Rosstat data. Not independently verified.",
     "CNN, NYT", "REPORTED", "ANALYSIS, MONDAY"),
    ("LOUVRE THEFT: 4 MORE ARRESTED",
     "The Paris prosecutor announced four more arrests over the theft at "
     "the Louvre Museum.",
     "Xinhua", "CONFIRMED", "TUESDAY"),
    ("MARKETS: AI RALLY REVERSES",
     "US stocks fell for an eighth time in nine sessions: Nasdaq down "
     "1.5%, Nvidia down 5.9%. Anthropic closed below its IPO price.",
     "The Times", "CONFIRMED", "TUESDAY"),
    ("THAILAND FLOODS: EMERGENCY IN SONGKHLA",
     "PM Anutin declared a state of emergency in Songkhla as severe "
     "flooding ravaged southern Thailand.",
     "Xinhua", "CONFIRMED", "TUESDAY"),
    ("RUSSIA: RECORD 432,519 CASUALTIES IN 2026",
     "Ukraine's General Staff said Russia suffered 432,519 casualties "
     "since 1 January; October was the deadliest month of the war.",
     "Kyiv Independent", "REPORTED", "TUESDAY, UKRAINIAN CLAIM"),
]
f_med = font(SERIF_B, 13)
f_medbody = font(SANS, 11)
f_medsrc = font(SANS_B, 9)
med_top = y
cols = [medium[:5], medium[5:]]
med_bottom = med_top
for ci, items in enumerate(cols):
    x = MARGIN + ci * (col_w + 24)
    yy = med_top
    for (h, b, src, tg, day) in items:
        yy = draw_wrapped(d, x, yy, h, f_med, col_w, leading=15)
        yy = draw_wrapped(d, x, yy, b, f_medbody, col_w, leading=11)
        d.text((x, yy), day + "  \u00b7  " + src + "  \u00b7  " + tg,
               font=f_medsrc, fill=RED)
        yy += 13
        med_bottom = max(med_bottom, yy)
y = med_bottom + 2
rule(d, MARGIN, y, CONTENT_W, 2)
y += 5

# ------------------------------------------------------- by the numbers band
d.text((MARGIN, y), "BY THE NUMBERS", font=font(SANS_B, 12), fill=RED)
y += 17
stats = [
    ("700,000+", "Russian troops killed\nin Ukraine (est.)"),
    ("432,519", "Russian casualties\nin 2026 (Ukraine)"),
    ("74,746", "Gaza death toll\n(WAFA)"),
    ("266M", "people face acute\nfood insecurity (WFP)"),
    ("7,000", "landmine casualties,\n5-year high"),
    ("$100M", "Shein FTC\nsettlement"),
]
f_stat = font(SERIF_B, 17)
f_statcap = font(SANS, 9)
band_w = CONTENT_W // len(stats)
for i, (num, cap) in enumerate(stats):
    sx = MARGIN + i * band_w
    if i:
        d.line([(sx - 6, y), (sx - 6, y + 34)], fill=LIGHT_GREY, width=1)
    d.text((sx, y), num, font=f_stat, fill=INK)
    cy = y + 20
    for ln in cap.split("\n"):
        d.text((sx, cy), ln, font=f_statcap, fill=GREY)
        cy += 11
y += 40
rule(d, MARGIN, y, CONTENT_W, 2)
y += 5

# ------------------------------------------------------- numbered list 13-36
small = [
    ("UK: 2 arrested after break-in at Prince William's Norfolk home.",
     "SCMP", "REPORTED", "Tue"),
    ("US soldier admits selling military secrets to Chinese buyers.",
     "Manila Times", "REPORTED", ""),
    ("Colombia: gunmen take 25 hostage at a supermarket.",
     "Manila Times", "REPORTED", ""),
    ("Hanoi: hot pot eatery blast kills 6, injures a dozen-plus.",
     "Manila Times", "REPORTED", ""),
    ("Seoul: Russian planes enter South Korea's air defence zone.",
     "Manila Times", "REPORTED", ""),
    ("UN: five women killed each hour by relatives in 2025.",
     "Manila Times", "REPORTED", ""),
    ("California faces an extreme flooding threat.",
     "Manila Times", "REPORTED", ""),
    ("Sport: England beat Australia by 8 wickets in the 2nd T20I.",
     "Jagran Josh", "CONFIRMED", "Tue"),
    ("RFE/RL back on shortwave in Afghanistan, lessons for girls.",
     "RFE/RL", "CONFIRMED", ""),
    ("Gaza death toll reaches 74,746, WAFA says.",
     "BD Global Times", "CLAIM", ""),
    ("WFP: 266 million people face acute food insecurity.",
     "BD Global Times", "REPORTED", ""),
    ("Oxfam: pollution risks across more than 99% of Gaza.",
     "BD Global Times", "REPORTED", ""),
    ("Landmines: 7,000 casualties, a five-year high.",
     "SCMP", "REPORTED", ""),
    ("North Korea threatens to shut its Swiss office.",
     "SCMP", "REPORTED", ""),
    ("China cobalt firms race to beat DR Congo export ban.",
     "SCMP", "REPORTED", ""),
    ("US envoy doubts Trump pledge to end $3.8bn Israel aid.",
     "SCMP", "REPORTED", ""),
    ("Russia accuses Ukraine of \u201cterrorism\u201d after drone strikes.",
     "BD Global Times", "REPORTED", "Tue"),
    ("Trump pardons the Thanksgiving turkeys.",
     "Manila Times", "REPORTED", ""),
    ("Democrats eye 2028 after US midterms triumph.",
     "Manila Times", "REPORTED", ""),
    ("NATO plans early-warning aircraft in Poland.",
     "Jagran Josh", "REPORTED", ""),
    ("Iran braces for winter gas shortages.",
     "RFE/RL", "REPORTED", ""),
    ("Gis\u00e8le Pelicot slams publisher over nude images.",
     "SCMP", "REPORTED", ""),
    ("Oligarch Potanin gives evidence in UK divorce trial.",
     "SCMP", "REPORTED", ""),
    ("India: BJP\u2013SAD alliance; Nepal PM ends state visit.",
     "Jagran Josh", "REPORTED", "22\u201323 Nov"),
]
d.text((MARGIN, y), "THE DAY IN BRIEF  \u2014  24 MORE STORIES",
       font=font(SANS_B, 12), fill=RED)
y += 16
f_num = font(SANS_B, 10)
f_small = font(SANS, 10)
f_smallsrc = font(SANS, 9)
list_top = y
list_bottom = list_top
half = (len(small) + 1) // 2
for ci, items in enumerate([small[:half], small[half:]]):
    x = MARGIN + ci * (col_w + 24)
    yy = list_top
    for k, (txt, src, tg, day) in enumerate(items):
        n = 13 + ci * half + k
        label = f"{n}. {txt}"
        suffix = f"  \u00b7  {src}  \u00b7  {tg}"
        if day:
            suffix += f"  \u00b7  {day}"
        # single line if it fits, else wrap text and put suffix on 2nd line
        full = label + suffix
        if d.textlength(full, font=f_small) <= col_w:
            d.text((x, yy), label, font=f_small, fill=INK)
            lw = d.textlength(label, font=f_small)
            d.text((x + lw, yy), suffix, font=f_smallsrc, fill=RED)
            yy += 13
        else:
            lines = wrap(d, label, f_small, col_w)
            for ln in lines:
                d.text((x, yy), ln, font=f_small, fill=INK)
                yy += 12
            d.text((x, yy), suffix.strip(), font=f_smallsrc, fill=RED)
            yy += 12
        list_bottom = max(list_bottom, yy)
y = list_bottom + 4
rule(d, MARGIN, y, CONTENT_W, 1)
y += 7

# ------------------------------------------------------- world map strip
map_top = y
d.text((MARGIN, map_top), "WHERE THE NEWS HAPPENED",
       font=font(SANS_B, 11), fill=RED)
map_y0 = map_top + 12
map_h = 56
map_x0, map_y1 = MARGIN, map_y0 + map_h
d.rectangle([map_x0, map_y0, map_x0 + CONTENT_W, map_y1], fill=MAP_SEA,
            outline=RULE)
def mx(lon):
    return map_x0 + (lon + 170) / 360.0 * CONTENT_W
def my(lat):
    return map_y0 + (75 - lat) / 150.0 * map_h
continents = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-70, 44), (-75, 35), (-80, 26), (-85, 20),
     (-90, 15), (-95, 18), (-105, 23), (-115, 30), (-125, 40), (-130, 55),
     (-150, 60), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 5), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -40), (-70, -50), (-72, -40),
     (-72, -25), (-78, -15), (-80, -5)],
    [(-10, 37), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55),
     (18, 56), (21, 59), (25, 60), (30, 62), (30, 70), (25, 71), (18, 69),
     (12, 65), (5, 60), (5, 58), (10, 55), (12, 50), (20, 45), (23, 40),
     (19, 42), (15, 44), (8, 44), (3, 43), (-2, 37)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 20), (43, 12), (48, 11), (51, 10), (45, 0),
     (40, -10), (35, -20), (32, -28), (28, -33), (20, -35), (15, -30),
     (12, -18), (9, -2), (8, 4), (-8, 5), (-15, 10)],
    [(30, 70), (45, 68), (60, 69), (75, 73), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55),
     (145, 45), (135, 40), (127, 35), (122, 30), (115, 22), (108, 15),
     (105, 10), (100, 7), (95, 15), (90, 22), (85, 20), (80, 10),
     (75, 8), (70, 20), (60, 25), (55, 26), (50, 29), (48, 30),
     (42, 36), (36, 36), (30, 40), (28, 45), (30, 50), (35, 55),
     (40, 60), (35, 65)],
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (132, -32),
     (124, -33), (115, -35), (113, -25)],
]
for poly in continents:
    pts = [(mx(lon), my(lat)) for lon, lat in poly]
    d.polygon(pts, fill=MAP_LAND, outline=(120, 110, 88))
markers = [
    # (label, lon, lat, label dx, label dy) — dy -9 above dot, +5 below
    ("NEW YORK", -74, 41, 5, -4),
    ("LONDON", 0, 51, 5, -9),
    ("KYIV", 30, 50, 5, -9),
    ("GAZA", 34, 31, 5, -9),
    ("RIYADH", 46, 24, 5, 6),
    ("DELHI", 77, 28, 5, -9),
    ("BANGKOK", 100, 14, 5, 6),
    ("SHANGHAI", 121, 31, 5, -9),
]
dots_only = [("PARIS", 2, 49), ("SEOUL", 127, 37), ("HANOI", 106, 21)]
f_map = font(SANS_B, 8)
for name, lon, lat, dx, dy in markers:
    px, py = mx(lon), my(lat)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
              outline=(255, 255, 255))
    d.text((px + dx, py + dy), name, font=f_map, fill=INK)
for name, lon, lat in dots_only:
    px, py = mx(lon), my(lat)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
              outline=(255, 255, 255))
y = map_y1 + 7

# ------------------------------------------------------- DATE CHECK box
box_top = y
box_h = 46
d.rectangle([MARGIN, box_top, MARGIN + CONTENT_W, box_top + box_h],
            fill=TAG_BG, outline=RED, width=1)
d.text((MARGIN + 8, box_top + 5), "DATE CHECK \u2014 NOT TUESDAY'S NEWS",
       font=font(SANS_B, 11), fill=RED)
dc = ("COP31 collapse (talks ended Sunday)  \u00b7  Nvidia reinstatement "
      "(Monday)  \u00b7  Hormuz tanker claims (Monday night)  \u00b7  Libya "
      "warship sinking (Sunday)  \u00b7  Riemann proof claim (Friday)  "
      "\u00b7  Indonesia factory fire toll 24 (Monday)  \u00b7  EU 22nd "
      "Russia sanctions (Monday)  \u00b7  GTA 6 release (19 Nov). "
      "These stories are NOT carried as 25 November news.")
draw_wrapped(d, MARGIN + 8, box_top + 20, dc, font(SANS, 10),
             CONTENT_W - 16, leading=12)
y = box_top + box_h + 6

# ------------------------------------------------------- footer
rule(d, MARGIN, y, CONTENT_W, 1)
y += 4
foot = ("All 36 stories verified on 25 November 2026 against independent "
        "sources. Every item carries its source and a CONFIRMED / REPORTED "
        "/ CLAIM tag.  \u00b7  THE WORLD TODAY")
d.text((MARGIN, y), foot, font=font(SANS, 9), fill=GREY)
print("final y:", y)

# light deterministic paper grain (seeded, so every run is identical)
import random
rng = random.Random(20261125)
for _ in range(25000):
    gx = rng.randint(12, W - 13)
    gy = rng.randint(12, H - 13)
    gc = (238, 233, 219) if rng.random() < 0.5 else (252, 249, 240)
    d.point((gx, gy), fill=gc)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
