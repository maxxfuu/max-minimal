import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("tokenembed")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

s.text(300, 8, "Token embedding: an ID becomes a d-dimensional vector", size=17, anchor="center")

# ------------------------------------------------ top: the lookup, one token -> one row vector
s.box(20, 76, 96, 44, "bats", size=16, stroke=BLUE, bg=BG_BLUE)
s.text(68, 128, "22526", size=13, color=GRAY, anchor="center")
s.arrow([(126, 98), (186, 98)], stroke=GRAY)

VALS = ["0.21", "-0.77", "0.05", "...", "0.63"]
X0, Y0, CW, CH = 196, 76, 60, 44
for i, v in enumerate(VALS):
    s.sbox(X0 + i * CW, Y0, CW, CH, v, size=13, stroke=BLUE, bg=BG_BLUE, sw=1)
W = CW * len(VALS)
s.sq(X0, Y0, W, CH, stroke=BLUE, sw=2)
s.line([(X0 + 2, Y0 - 12), (X0 + W - 2, Y0 - 12)], stroke=GRAY, sw=1)
s.line([(X0 + 2, Y0 - 12), (X0 + 2, Y0 - 4)], stroke=GRAY, sw=1)
s.line([(X0 + W - 2, Y0 - 12), (X0 + W - 2, Y0 - 4)], stroke=GRAY, sw=1)
s.text(X0 + W / 2, Y0 - 18, "d", size=13, color=GRAY, anchor="center", valign="bottom")

# ------------------------------------------------ bottom: where the vectors live, similar words close
BX, BY, BW, BH = 40, 180, 520, 200
s.arrow([(BX, BY + BH), (BX + BW, BY + BH)], stroke=BLACK, sw=1)   # x axis
s.arrow([(BX, BY + BH), (BX, BY)], stroke=BLACK, sw=1)             # y axis
s.text(BX + BW + 8, BY + BH, "x", size=13, valign="middle")
s.text(BX, BY - 8, "y", size=13, anchor="center", valign="bottom")
s.text(BX + BW / 2, BY + BH + 10, "embedding space", size=12, color=GRAY, anchor="center")

s.ellipse(80, 220, 170, 110, stroke=GRAY, ss="dashed", sw=1)
s.ellipse(330, 240, 170, 110, stroke=GRAY, ss="dashed", sw=1)

POINTS = [
    (120, 262, "owls", BLACK), (196, 250, "cats", BLACK), (166, 300, "bats", BLUE),
    (372, 284, "car", BLACK), (446, 272, "truck", BLACK), (414, 322, "bus", BLACK),
]
for x, y, lab, col in POINTS:
    s.ellipse(x - 5, y - 5, 10, 10, stroke=col, bg=col, sw=1)
    s.text(x, y - 10, lab, size=13, anchor="center", valign="bottom")

s.save(os.path.join(OUT, "token-embedding.excalidraw"))
