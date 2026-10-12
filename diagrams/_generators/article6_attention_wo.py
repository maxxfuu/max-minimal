import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("attnwo")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

TOKENS = ["I", "love", "to", "study", "bats"]
C = 40


def matrix(x, y, rows, stroke, bg, fill="solid", tokens=False, dim_text=None, dim_color=BLACK):
    w, h = C * len(rows[0]), C * len(rows)
    for r, row in enumerate(rows):
        yy = y + r * C
        if tokens:
            s.text(x - 12, yy + C / 2, TOKENS[r], size=14, anchor="right", valign="middle")
        for c, v in enumerate(row):
            s.sbox(x + c * C, yy, C, C, v, size=12, stroke=stroke, bg=bg, fill=fill, sw=1)
    s.sq(x, y, w, h, stroke=stroke, sw=2)
    if dim_text:
        s.text(x + w / 2, y + h + 8, dim_text, size=13, color=dim_color, anchor="center")
    return w, h


# matmul on paper: O bottom-left, W_O top-right, output bottom-right
O = [
    ["0.4", "-0.2", "..."],
    ["0.8", "0.2", "..."],
    ["0.4", "0.3", "..."],
    ["0.4", "0.0", "..."],
    ["0.5", "0.2", "..."],
]
WO = [
    ["0.3", "-0.1", "0.5", "...", "0.2"],
    ["-0.4", "0.6", "0.1", "...", "-0.3"],
    ["...", "...", "...", "...", "..."],
]
OUTM = [
    ["0.1", "-0.2", "0.2", "...", "0.1"],
    ["0.2", "0.0", "0.4", "...", "0.1"],
    ["0.0", "0.1", "0.2", "...", "0.0"],
    ["0.1", "-0.1", "0.2", "...", "0.1"],
    ["0.1", "0.1", "0.3", "...", "0.0"],
]
OX, TOP, GAP = 110, 70, 44
OW = C * len(O[0])
WX = OX + OW + GAP
WW, WH = matrix(WX, TOP, WO, TEAL, BG_CYAN, dim_text="W_O  (d_v x d)", dim_color=TEAL)
BOT = TOP + WH + GAP + 12
s.text(OX + (WX + WW - OX) / 2, 8, "O W_O", size=17, anchor="center")
matrix(OX, BOT, O, ORANGE_D, BG_ORANGE, tokens=True, dim_text="O  (n x d_v)", dim_color=ORANGE_D)
matrix(WX, BOT, OUTM, TEAL, BG_CYAN, fill="hachure", dim_text="output  (n x d)", dim_color=TEAL)

s.save(os.path.join(OUT, "attention-wo.excalidraw"))
