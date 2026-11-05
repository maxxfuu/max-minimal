import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page12")

BL_ST, BL_BG = "#1971c2", "#a5d8ff"
RD, RD_BG = "#fa5252", "#ffe3e3"
CW = 24          # cell width for the 32 lanes and 32 banks
LANE_Y, BANK_Y = 150, 330
X0 = 40


def used_of(bank_of):
    u = {}
    for i in range(32):
        u[bank_of(i)] = u.get(bank_of(i), 0) + 1
    return u


def figure(fname, scene, title, formula, bank_of, verdict, note):
    s = Scene(scene)
    used = used_of(bank_of)
    s.text(X0, 12, title, size=24)
    s.text(X0, 48, "BK = 16, so innerRowA = lane / 4 and innerColA = lane % 4   ·   one warp, the j = 0 store of its float4",
           size=13, color=GRAY)
    s.text(X0, 96, formula, size=15)
    # lanes
    s.text(X0, LANE_Y - 20, "lane", size=11, color=GRAY_D)
    for i in range(32):
        s.sq(X0 + i * CW, LANE_Y, CW, CW, stroke=BL_ST, bg=BL_BG, fill="solid", sw=1)
        if i % 4 == 0:
            s.text(X0 + i * CW + CW / 2, LANE_Y + CW + 4, str(i), size=10, color=GRAY_D, anchor="center")
    # banks
    s.text(X0, BANK_Y - 20, "bank", size=11, color=GRAY_D)
    for b in range(32):
        n = used.get(b, 0)
        st, bg = (RD, RD_BG) if n > 1 else ((GREEN, BG_GREEN) if n == 1 else (GRAY, NONE))
        s.sq(X0 + b * CW, BANK_Y, CW, CW, stroke=st, bg=bg, fill="solid", sw=1)
        if n:
            s.text(X0 + b * CW + CW / 2, BANK_Y + CW / 2, str(n), size=12, anchor="center", valign="middle")
        if b % 4 == 0:
            s.text(X0 + b * CW + CW / 2, BANK_Y + CW + 4, str(b), size=10, color=GRAY_D, anchor="center")
    # lane -> bank lines
    for i in range(32):
        b = bank_of(i)
        s.line([(X0 + i * CW + CW / 2, LANE_Y + CW), (X0 + b * CW + CW / 2, BANK_Y)],
               stroke=GRAY, sw=1, roundness=SHARP, opacity=70)
    s.text(X0, BANK_Y + 50, verdict, size=14)
    s.text(X0, BANK_Y + 76, note, size=12, color=GRAY_D)
    s.save(os.path.join(OUT, fname + ".excalidraw"))


# before: A_STRIDE = 128, the column term vanishes
figure("bank-conflicts-before", "bankbefore",
       "Bank conflicts on the transposed store  -  before padding",
       "A_STRIDE = 128      bank = innerRowA mod 32",
       lambda i: (i // 4) % 32,
       "8 banks hit, 4 lanes each  →  4-way conflict",
       "(128 · (4·innerColA + j)) mod 32 = 0, the column term contributes nothing")

# after: A_STRIDE = 130
figure("bank-conflicts-after", "bankafter",
       "Bank conflicts on the transposed store  -  after padding",
       "A_STRIDE = 130      bank = (2·(4·innerColA + j) + innerRowA) mod 32",
       lambda i: (2 * (4 * (i % 4) + 0) + i // 4) % 32,
       "32 banks hit, 1 lane each  →  no conflict",
       "130 mod 32 = 2, so innerColA = 0..3 lands on banks 0, 8, 16, 24 plus innerRowA")
