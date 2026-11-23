#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

News facts verified against live reporting on 22-23 Nov 2026 (AP, AFP,
Reuters, CNN, Al Jazeera, Korea Herald). Layout: newspaper front page,
masthead, one lead story, six stories in a 3x2 grid. Deterministic:
same input -> same bytes (no timestamps, no randomness). Every block
is measured before it is drawn; asserts guard overflow.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 48  # margin
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (244, 241, 234)
INK = (26, 26, 26)
BODY = (85, 85, 85)
FAINT = (136, 136, 136)
RED = (139, 0, 0)
HAIR = (208, 207, 203)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width, limit=None):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if limit is not None:
        assert len(lines) <= limit, (text, lines)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# (kicker, headline, body, sources)
STORIES = [
    ("WASHINGTON", "Democrats win biggest House majority since 1992",
     "A North Carolina recount hands Democrats their 258th seat as "
     "Chuck Hubbard beats Virginia Foxx by 330 votes.", "AP, CNN"),
    ("CARACAS", "US and Venezuela restore military ties",
     "The two countries sign a deal to reestablish military ties as "
     "the US defence chief visits Caracas.", "AP"),
    ("LIBYA", "Drone strike hits Russian warship at Benghazi",
     "A suspected sea drone hits the Russian corvette Merkury at "
     "its Benghazi naval base, setting it ablaze.", "AP"),
    ("SUDAN", "Drones kill four near Khartoum, hit UN building",
     "Attacks blamed on the RSF kill four around Sudan's capital "
     "and damage a United Nations building.", "AFP"),
    ("UKRAINE", "Zelenskyy pleads for Patriots as Kyiv reels",
     "Ukraine's president urges the US to release Patriot missiles "
     "as Russian strikes leave 14 missing in Kyiv region.", "AP"),
    ("MEXICO", "Cartel boss 'El Chapo Isidro' captured",
     "Mexican forces seize cartel leader Fausto Isidro Meza Flores "
     "in a Sinaloa gun battle that leaves 11 dead.", "AP"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 40

    # ---- top eyebrow ----
    f_eyebrow = font(SANS_B, 20)
    d.text((M, y), "THE WORLD IN ONE IMAGE", font=f_eyebrow, fill=RED)
    right = "SUNDAY"
    d.text((W - M - d.textlength(right, font=f_eyebrow), y), right,
           font=f_eyebrow, fill=INK)
    y += 30
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 14

    # ---- masthead (fit to width) ----
    size = 64
    f_mast = font(SERIF_B, size)
    title = "THE WORLD TODAY"
    while d.textlength(title, font=f_mast) > W - 2 * M and size > 40:
        size -= 2
        f_mast = font(SERIF_B, size)
    d.text(((W - d.textlength(title, font=f_mast)) / 2, y), title,
           font=f_mast, fill=INK)
    y += size + 10

    # ---- date line ----
    f_date = font(SERIF, 30)
    date = "Sunday, 22 November 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, y), date,
           font=f_date, fill=INK)
    y += 44
    d.line([(M, y), (W - M, y)], fill=INK, width=5)
    y += 9
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 16

    # ---- lead story ----
    f_kick = font(SANS_B, 21)
    d.text((M, y), "TOP STORY  \u2022  ANTALYA, TURKEY", font=f_kick,
           fill=RED)
    y += 31
    f_head = font(SERIF_B, 44)
    head_lines = wrap(d, "COP31 collapses with no deal as "
                         "fossil-fuel rift splits summit",
                      f_head, W - 2 * M, limit=3)
    y = text_block(d, M, y, head_lines, f_head, INK, 52)
    y += 6
    f_deck = font(SANS, 19)
    deck = ("The UN climate talks in Antalya end empty-handed after "
            "the EU and island states reject a final text that never "
            "names fossil fuels; the summit runs into record overtime "
            "and fails.")
    y = text_block(d, M, y, wrap(d, deck, f_deck, W - 2 * M, limit=3),
                   f_deck, BODY, 26)
    y += 6
    f_src = font(SANS, 17)
    d.text((M, y), "Sources: AFP, AP", font=f_src, fill=FAINT)
    y += 28

    # ---- divider, then 3-col x 2-row grid ----
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 16
    grid_top = y

    gap = 24
    col_w = (W - 2 * M - 2 * gap) // 3
    f_ck = font(SANS_B, 18)
    f_ch = font(SERIF_B, 24)
    f_cb = font(SANS, 15)
    f_cs = font(SANS, 11)

    # measure every cell first
    cells = []
    for kick, head, body, src in STORIES:
        head_lines = wrap(d, head, f_ch, col_w, limit=3)
        body_lines = wrap(d, body, f_cb, col_w, limit=4)
        height = 26 + len(head_lines) * 29 + 6 + len(body_lines) * 20 + 4 + 16
        cells.append((kick, head_lines, body_lines, src, height))
    row0_h = max(c[4] for c in cells[:3])
    row1_h = max(c[4] for c in cells[3:])
    grid_bottom = grid_top + row0_h + 16 + row1_h
    assert grid_bottom < 930, grid_bottom

    for i, (kick, head_lines, body_lines, src, _h) in enumerate(cells):
        cx = M + (i % 3) * (col_w + gap)
        cy = grid_top if i < 3 else grid_top + row0_h + 16
        d.text((cx, cy), kick, font=f_ck, fill=RED)
        hy = text_block(d, cx, cy + 26, head_lines, f_ch, INK, 29)
        by = text_block(d, cx, hy + 6, body_lines, f_cb, BODY, 20)
        d.text((cx, by + 4), src.upper(), font=f_cs, fill=FAINT)

    # vertical separators between columns
    for c in (1, 2):
        x = M + c * col_w + (c - 1) * gap + gap // 2
        d.line([(x, grid_top + 4), (x, grid_top + row0_h - 6)],
               fill=HAIR, width=2)
        d.line([(x, grid_top + row0_h + 16 + 4),
                (x, grid_top + row0_h + 16 + row1_h - 6)],
               fill=HAIR, width=2)

    # ---- footer ----
    fy = grid_bottom + 12
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    f_foot = font(SANS, 17)
    foot = ("Also: Baltic cargo ship ablaze after a drone strike; "
            "French protests, sixth weekend; Brazil storm kills four. "
            "Sources: AP, AFP, CNN, Reuters \u2014 all events "
            "of 22 November 2026.")
    foot_lines = wrap(d, foot, f_foot, W - 2 * M, limit=2)
    bottom = fy + 12 + len(foot_lines) * 23
    assert bottom <= 1010, bottom
    text_block(d, M, fy + 12, foot_lines, f_foot, FAINT, 23)

    out = "/home/hatch/workspace/makefun/work/news-image-20261122/repo/entry.png"
    img.save(out, "PNG", optimize=True)
    print("wrote", out, "grid_top", grid_top, "row0", row0_h, "row1",
          row1_h, "grid_bottom", grid_bottom, "bottom", bottom)


if __name__ == "__main__":
    main()
