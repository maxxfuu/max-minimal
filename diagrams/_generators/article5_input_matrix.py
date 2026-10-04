import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("inputmatrix")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

s.text(431, 8, "Stacking embedded vectors into the input matrix X", size=17, anchor="center")

# ------------------------------------------------ the input matrix: one row per token
TOKENS = ["I", "love", "to", "study", "bats"]
ROWS = [
    ["0.42", "-0.18", "0.91", "0.07", "...", "-0.55"],
    ["-0.33", "0.64", "0.12", "-0.80", "...", "0.29"],
    ["0.08", "0.15", "-0.47", "0.36", "...", "0.71"],
    ["0.59", "-0.92", "0.24", "0.50", "...", "-0.06"],
    ["0.21", "-0.77", "0.05", "-0.12", "...", "0.63"],
]
X0, Y0, CW, CH = 150, 84, 68, 44
W, H = CW * len(ROWS[0]), CH * len(ROWS)

s.text(X0 - 22, Y0 - 14, "tokens", size=12, color=GRAY, anchor="right", valign="bottom")
for r, (tok, row) in enumerate(zip(TOKENS, ROWS)):
    y = Y0 + r * CH
    s.text(X0 - 22, y + CH / 2, tok, size=18, anchor="right", valign="middle")
    for c, v in enumerate(row):
        s.sbox(X0 + c * CW, y, CW, CH, v, size=15, stroke=BLUE, bg=BG_BLUE, sw=1)
s.sq(X0, Y0, W, H, stroke=BLUE, sw=2)

# d across the top, n down the right
s.line([(X0 + 2, Y0 - 14), (X0 + W - 2, Y0 - 14)], stroke=GRAY, sw=1)
s.line([(X0 + 2, Y0 - 14), (X0 + 2, Y0 - 6)], stroke=GRAY, sw=1)
s.line([(X0 + W - 2, Y0 - 14), (X0 + W - 2, Y0 - 6)], stroke=GRAY, sw=1)
s.text(X0 + W / 2, Y0 - 20, "d dimensions", size=13, color=GRAY, anchor="center", valign="bottom")

s.text(X0 + W / 2, Y0 + H + 14, "X: one embedded vector per row (n tokens x d)",
       size=14, color=BLUE, anchor="center")

# ------------------------------------------------ into the Query and Key matrices
AX = X0 + W + 12
MID = Y0 + H / 2
s.arrow([(AX, MID - 14), (AX + 62, MID - 52)], stroke=GRAY)
s.arrow([(AX, MID + 14), (AX + 62, MID + 52)], stroke=GRAY)
s.box(AX + 72, MID - 86, 96, 60, "W_Q", size=18, stroke=RED, bg=BG_RED)
s.box(AX + 72, MID + 26, 96, 60, "W_K", size=18, stroke=GREEN, bg=BG_GREEN)
s.text(AX + 180, MID - 56, "Query", size=13, color=RED, valign="middle")
s.text(AX + 180, MID + 56, "Key", size=13, color=GREEN, valign="middle")

s.text(431, Y0 + H + 52, "the whole sequence moves through the weights as one matrix, not one vector at a time",
       size=13, color=GRAY, anchor="center")

s.save(os.path.join(OUT, "input-matrix.excalidraw"))
