import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("attnav")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

TOKENS = ["I", "love", "to", "study", "bats"]
C = 40
YELLOW = "#e67700"   # stroke to go with BG_YELLOW


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


# matmul on paper: A bottom-left, V top-right, O bottom-right
A = [   # softmax of the scores, causal so each row only looks back
    ["1.0", "0", "0", "0", "0"],
    ["0.3", "0.7", "0", "0", "0"],
    ["0.2", "0.5", "0.3", "0", "0"],
    ["0.1", "0.4", "0.1", "0.4", "0"],
    ["0.1", "0.5", "0.1", "0.1", "0.2"],
]
V = [
    ["0.4", "-0.2", "..."],
    ["0.9", "0.3", "..."],
    ["-0.5", "0.6", "..."],
    ["0.2", "-0.7", "..."],
    ["0.8", "0.1", "..."],
]
O = [
    ["0.4", "-0.2", "..."],
    ["0.8", "0.2", "..."],
    ["0.4", "0.3", "..."],
    ["0.4", "0.0", "..."],
    ["0.5", "0.2", "..."],
]
AX, TOP, GAP = 110, 70, 44
AW = C * len(A[0])
VX = AX + AW + GAP
VW, VH = matrix(VX, TOP, V, YELLOW, BG_YELLOW, dim_text="V  (n x d_v)", dim_color=YELLOW)
BOT = TOP + VH + GAP + 12
s.text(AX + (VX + VW - AX) / 2, 8, "O = A V", size=17, anchor="center")
for c, tok in enumerate(TOKENS):
    s.text(AX + c * C + C / 2, BOT - 8, tok, size=12, anchor="center", valign="bottom")
matrix(AX, BOT, A, VIOLET, BG_VIOLET, fill="hachure", tokens=True,
       dim_text="A: attention scores  (n x n)", dim_color=VIOLET)
matrix(VX, BOT, O, ORANGE_D, BG_ORANGE, dim_text="O  (n x d_v)", dim_color=ORANGE_D)

s.save(os.path.join(OUT, "attention-av.excalidraw"))
