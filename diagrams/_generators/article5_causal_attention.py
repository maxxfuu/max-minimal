import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("causalattn")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

TOKENS = ["I", "love", "to", "study", "bats"]
N = len(TOKENS)
C = 44            # cell size
CX = 470

s.text(CX, 8, "Causal attention: a token only scores against itself and what came before", size=17, anchor="center")

# raw scores (lower triangle of S from the previous figure) and the softmaxed rows
S = [
    ["1.9"],
    ["0.5", "2.3"],
    ["-0.3", "0.2", "1.5"],
    ["0.7", "-0.6", "1.0", "2.1"],
    ["1.2", "0.4", "-0.1", "0.6", "1.8"],
]
A = [
    ["1.0"],
    ["0.3", "0.7"],
    ["0.2", "0.5", "0.3"],
    ["0.1", "0.4", "0.1", "0.4"],
    ["0.1", "0.5", "0.1", "0.1", "0.2"],
]
Y0 = 96
W = H = C * N


def masked_grid(x, y, rows, stroke, bg, keys=True):
    """lower triangle filled and valued, upper triangle greyed out, with the
    staircase that separates them drawn heavy so the diagonal reads at a glance"""
    if keys:   # keys across the top, queries down the side
        for c, tok in enumerate(TOKENS):
            s.text(x + c * C + C / 2, y - 8, tok, size=13, anchor="center", valign="bottom")
    for r, row in enumerate(rows):
        for c in range(N):
            if c <= r:
                s.sbox(x + c * C, y + r * C, C, C, row[c], size=13, stroke=stroke, bg=bg, fill="hachure", sw=1)
            else:
                s.sbox(x + c * C, y + r * C, C, C, "-", size=13, color=GRAY, stroke=GRAY, ss="dashed", sw=1)
    s.sq(x, y, W, H, stroke=stroke, sw=2)
    # the staircase: from the top-left corner down to the bottom-right corner
    pts = [(x, y)]
    for i in range(N):
        pts.append((x + (i + 1) * C, y + i * C))
        pts.append((x + (i + 1) * C, y + (i + 1) * C))
    s.line(pts, stroke=stroke, sw=3, roundness=SHARP)


# ------------------------------------------------ left: masked scores, one query row per token
LX = 120
for r, tok in enumerate(TOKENS):
    s.text(LX - 12, Y0 + r * C + C / 2, tok, size=13, anchor="right", valign="middle")
masked_grid(LX, Y0, S, VIOLET, BG_VIOLET)
s.text(LX + W / 2, Y0 + H + 8, "S = Q K^T, future keys masked", size=13, color=VIOLET, anchor="center")

# ------------------------------------------------ middle: a softmax over each row
BX = LX + W + 36
BW = 84
for r in range(N):
    my = Y0 + r * C + C / 2
    s.arrow([(LX + W + 6, my), (BX - 6, my)], stroke=GRAY, sw=1)
    s.box(BX, my - 14, BW, 28, "softmax", size=12, stroke=GRAY_D, bg=BG_GRAY, sw=1)
    s.arrow([(BX + BW + 6, my), (BX + BW + 36 - 6, my)], stroke=GRAY, sw=1)
s.text(BX + BW / 2, Y0 - 8, "per row", size=12, color=GRAY, anchor="center", valign="bottom")

# ------------------------------------------------ right: the attention scores, each row sums to 1
RX = BX + BW + 36
masked_grid(RX, Y0, A, VIOLET, BG_VIOLET)
s.text(RX + W / 2, Y0 + H + 8, "A: attention scores, each row sums to 1", size=13, color=VIOLET, anchor="center")

s.save(os.path.join(OUT, "causal-attention.excalidraw"))
