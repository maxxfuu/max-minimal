import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("warptile")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page10")

RD, RD_BG = "#fa5252", "#ffe3e3"

s.text(60, 12, "Warp tiling  -  block tile → warp tile → sub-tile → thread patch", size=24)
s.text(60, 48, "BM × BN = 128 × 64,   WM × WN = 64 × 32,   WMITER × WNITER = 2 × 2,   TM × TN = 4 × 4,   128 threads = 4 warps",
       size=13, color=GRAY)

# ------------------------------------------------------------ block tile, 2.5 px per element
BX, BY, SC = 70, 130, 2.5
BW, BH = 64 * SC, 128 * SC
s.text(BX + BW / 2, BY - 22, "block tile of C   128 × 64", size=13, anchor="center")
s.sq(BX, BY, BW, BH, sw=2)
s.line([(BX + BW / 2, BY), (BX + BW / 2, BY + BH)], stroke=GRAY, sw=1, roundness=SHARP)
s.line([(BX, BY + BH / 2), (BX + BW, BY + BH / 2)], stroke=GRAY, sw=1, roundness=SHARP)
for i, (r, c) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
    s.text(BX + c * BW / 2 + BW / 4, BY + r * BH / 2 + BH / 4, "warp %d" % i, size=12, color=GRAY_D,
           anchor="center", valign="middle")
s.sq(BX, BY, BW / 2, BH / 2, stroke=GREEN, bg=BG_GREEN, fill="hachure", sw=3)
s.text(BX, BY + BH + 12, "warpRow = warpIdx / 2\nwarpCol = warpIdx % 2", size=11, color=GRAY_D, font=CODE)

# ------------------------------------------------------------ warp tile, 5 px per element
WX, WY, SC2 = 330, 130, 5
WW, WH = 32 * SC2, 64 * SC2
s.text(WX, WY - 22, "warp tile   64 × 32", size=13, color=GREEN)
s.line([(BX + BW / 2, BY), (WX, WY)], stroke=GRAY, ss="dashed", sw=1, roundness=SHARP)
s.line([(BX + BW / 2, BY + BH / 2), (WX, WY + WH)], stroke=GRAY, ss="dashed", sw=1, roundness=SHARP)
s.sq(WX, WY, WW, WH, stroke=GREEN, sw=2)
s.line([(WX + WW / 2, WY), (WX + WW / 2, WY + WH)], stroke=GRAY, sw=1, roundness=SHARP)
s.line([(WX, WY + WH / 2), (WX + WW, WY + WH / 2)], stroke=GRAY, sw=1, roundness=SHARP)
for r in range(2):
    for c in range(2):
        s.text(WX + c * WW / 2 + WW / 4, WY + r * WH / 2 + WH / 4, "sub (%d,%d)" % (r, c), size=11,
               color=GRAY_D, anchor="center", valign="middle")
s.sq(WX, WY, WW / 2, WH / 2, stroke=GREEN, bg=BG_GREEN, fill="hachure", sw=3)
s.text(WX, WY + WH + 12, "WMITER = 2 down, WNITER = 2 across\nWSUBM × WSUBN = 32 × 16", size=11, color=GRAY_D, font=CODE)

# ------------------------------------------------------------ sub-tile, 10 px per element
SX, SY, SC3 = 610, 130, 10
SW, SH = 16 * SC3, 32 * SC3
s.text(SX, SY - 22, "sub-tile   32 × 16,  8 × 4 patches", size=13, color=GREEN)
s.line([(WX + WW / 2, WY), (SX, SY)], stroke=GRAY, ss="dashed", sw=1, roundness=SHARP)
s.line([(WX + WW / 2, WY + WH / 2), (SX, SY + SH)], stroke=GRAY, ss="dashed", sw=1, roundness=SHARP)
grid_box(s, SX, SY, SW, SH, 4, 8, stroke=GREEN, sw=2, line="#ced4da", ls="solid", bg=BG_GREEN, fill="hachure")
for t in range(32):
    r, c = t // 4, t % 4
    s.text(SX + c * SW / 4 + SW / 8, SY + r * SH / 8 + SH / 16, "t%d" % t, size=10, color=GRAY_D,
           anchor="center", valign="middle")
s.sq(SX + 3 * SW / 4, SY, SW / 4, SH / 8, stroke=RD, bg=RD_BG, fill="cross-hatch", sw=2)
s.arrow([(SX + SW + 70, SY + SH / 16), (SX + SW + 6, SY + SH / 16)], stroke=RD, sw=2)
s.text(SX + SW + 80, SY + 6, "one thread  →  a 4 × 4 patch", size=12, color=RD)
s.text(SX + SW + 80, SY + 26, "threadRowInWarp = 0,  threadColInWarp = 3", size=11, color=GRAY_D, font=CODE)
s.text(SX, SY + SH + 12, "32 threads = one warp, laid out 8 down × 4 across", size=11, color=GRAY_D, font=CODE)

# ------------------------------------------------------------ footprint, per dotIdx
FX, FY = SX + SW + 80, SY + 90
s.text(FX, FY, "warp footprint per dotIdx, per sub-tile", size=13)
s.text(FX, FY + 26, "As   32 floats  (WSUBM)", size=12, color=BLUE)
s.text(FX, FY + 46, "Bs   16 floats  (WSUBN)", size=12, color=CYAN)
s.text(FX, FY + 76, "kernel 7, same instruction:", size=12, color=GRAY_D)
s.text(FX, FY + 96, "Bs   128 floats, the whole BN", size=12, color=GRAY_D)

s.save(os.path.join(OUT, "warp-tiling-hierarchy.excalidraw"))
