import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("vectrans")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page9")

CY_ST, CY_BG = "#0c8599", "#99e9f2"
BL_ST, BL_BG = "#1971c2", "#a5d8ff"
CELL = 22

s.text(60, 12, "Vectorized loads  -  A is transposed on the way into shared memory", size=24)
s.text(60, 48, "BM = BN = 128,  BK = 8,  TM = TN = 8   ·   one thread moves one float4", size=13, color=GRAY)


def cell(x, y, st, bg, op=100):
    s.sq(x, y, CELL, CELL, stroke=st, bg=bg, fill="solid", sw=1, opacity=op)


# ============================================================ 1 · the store
s.rect(30, 86, 820, 340, sw=2, roundness=ROUND)
s.text(46, 98, "1 · Store   one float4 of A becomes four scalar stores into As", size=15)

# A tile in GMEM, [BM x BK] = 128 x 8, drawn as 8 columns x 10 rows (elided)
AX, AY = 130, 150
grid_box(s, AX, AY, 8 * CELL, 10 * CELL, 8, 10, stroke=BL_ST, sw=2, bg="#e3f6fb")
s.text(AX, AY - 22, "A tile in GMEM   [BM × BK] = 128 × 8", size=12, color=BL_ST)
s.text(AX + 4 * CELL, AY + 9 * CELL + 2, "...", size=14, color=GRAY, anchor="center")
for c in range(4):
    cell(AX + c * CELL, AY + 3 * CELL, BL_ST, BL_ST, 45)
s.text(AX - 8, AY + 3 * CELL + CELL / 2, "innerRowA", size=11, color=GRAY_D, anchor="right", valign="middle")
s.text(AX + 2 * CELL, AY + 3 * CELL - 14, "innerColA·4 .. +3", size=10, color=BL_ST, anchor="center")
s.text(AX, AY + 10 * CELL + 24, "one LDG.128, along K", size=12, color=GRAY_D)

# arrow to As
s.arrow([(AX + 8 * CELL + 16, AY + 3 * CELL + CELL / 2), (AX + 8 * CELL + 96, AY + 3 * CELL + CELL / 2)],
        stroke=BL_ST, sw=3)
s.text(AX + 8 * CELL + 56, AY + 3 * CELL - 8, "tmp.x .. tmp.w", size=11, color=BL_ST, anchor="center", font=CODE)

# As transposed, [BK x BM] = 8 x 128, drawn as 16 columns x 8 rows (elided)
TX, TY = 430, 150
grid_box(s, TX, TY, 16 * CELL, 8 * CELL, 16, 8, stroke=BL_ST, sw=2, bg=BL_BG, fill="hachure")
s.text(TX, TY - 22, "As in SMEM   [BK × BM] = 8 × 128,  stored As[k][m]", size=12, color=BL_ST)
s.text(TX + 16 * CELL + 12, TY + 4 * CELL, "...", size=14, color=GRAY, valign="middle")
for r in range(4):
    cell(TX + 3 * CELL, TY + r * CELL, BL_ST, BL_ST, 45)
s.text(TX + 3 * CELL + CELL / 2, TY + 8 * CELL + 4, "innerRowA", size=10, color=GRAY_D, anchor="center")
s.text(TX - 8, TY + 2 * CELL, "k = 0..3", size=11, color=GRAY_D, anchor="right", valign="middle")
s.text(TX, TY + 8 * CELL + 30, "four STS.32, BM floats apart   (no vector store possible)", size=12, color=GRAY_D)

# ============================================================ 2 · the read
s.rect(30, 452, 820, 372, sw=2, roundness=ROUND)
s.text(46, 464, "2 · Read   a thread's TM = 8 values of A, per dotIdx", size=15)

# kernel 6 layout: As[m][k], column read with stride BK
KX, KY = 130, 520
grid_box(s, KX, KY, 8 * CELL, 10 * CELL, 8, 10, stroke=GRAY_D, sw=2, bg=BG_GRAY)
s.text(KX, KY - 22, "kernel 6   As[m][k]", size=12, color=GRAY_D)
for r in range(2, 10):
    cell(KX + 2 * CELL, KY + r * CELL, GRAY_D, GRAY_D, 45)
s.text(KX + 2 * CELL + CELL / 2, KY + 10 * CELL + 4, "dotIdx", size=10, color=GRAY_D, anchor="center")
s.text(KX, KY + 10 * CELL + 30, "8 floats, BK apart", size=12, color=GRAY_D)
s.text(KX, KY + 10 * CELL + 50, "eight LDS.32", size=12, color=GRAY_D)

# kernel 7 layout: As[k][m], contiguous row read
RX, RY = 430, 520
grid_box(s, RX, RY, 16 * CELL, 8 * CELL, 16, 8, stroke=BL_ST, sw=2, bg=BL_BG, fill="hachure")
s.text(RX, RY - 22, "kernel 7   As[k][m]", size=12, color=BL_ST)
s.text(RX + 16 * CELL + 12, RY + 4 * CELL, "...", size=14, color=GRAY, valign="middle")
s.sq(RX + 4 * CELL, RY + 2 * CELL, 8 * CELL, CELL, stroke=BL_ST, bg=BL_ST, fill="solid", sw=1, opacity=45)
s.text(RX - 8, RY + 2 * CELL + CELL / 2, "dotIdx", size=11, color=GRAY_D, anchor="right", valign="middle")
s.text(RX + 8 * CELL, RY + 2 * CELL - 14, "threadRow·TM .. +7", size=10, color=BL_ST, anchor="center")
s.text(RX, RY + 8 * CELL + 10, "8 contiguous floats", size=12, color=BL_ST)
s.text(RX, RY + 8 * CELL + 30, "two LDS.128", size=12, color=BL_ST)

s.text(RX + 200, RY + 8 * CELL + 10, "Bs [BK × BN] is unchanged:", size=12, color=CY_ST)
s.text(RX + 200, RY + 8 * CELL + 30, "TN = 8 contiguous, two LDS.128", size=12, color=CY_ST)

s.save(os.path.join(OUT, "vectorized-transpose.excalidraw"))
