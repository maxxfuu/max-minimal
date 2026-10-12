import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("inputmatrix")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")


# ------------------------------------------------ the input matrix: one row per token
TOKENS = ["I", "love", "to", "study", "bats"]
ROWS = [
    ["0.42", "-0.18", "0.91", "...", "-0.55"],
    ["-0.33", "0.64", "0.12", "...", "0.29"],
    ["0.08", "0.15", "-0.47", "...", "0.71"],
    ["0.59", "-0.92", "0.24", "...", "-0.06"],
    ["0.21", "-0.77", "0.05", "...", "0.63"],
]
# square cells and as many columns as rows, so X is drawn as a square matrix
X0, Y0, CW, CH = 110, 70, 44, 44
W, H = CW * len(ROWS[0]), CH * len(ROWS)
CX = X0 + W / 2
s.text(CX, 8, "Stacking embedded vectors into the input matrix X", size=17, anchor="center")

s.text(X0 - 18, Y0 - 14, "tokens", size=12, color=GRAY, anchor="right", valign="bottom")
for r, (tok, row) in enumerate(zip(TOKENS, ROWS)):
    y = Y0 + r * CH
    s.text(X0 - 18, y + CH / 2, tok, size=14, anchor="right", valign="middle")
    for c, v in enumerate(row):
        s.sbox(X0 + c * CW, y, CW, CH, v, size=12, stroke=BLUE, bg=BG_BLUE, sw=1)
s.sq(X0, Y0, W, H, stroke=BLUE, sw=2)

# d across the top
s.line([(X0 + 2, Y0 - 14), (X0 + W - 2, Y0 - 14)], stroke=GRAY, sw=1)
s.line([(X0 + 2, Y0 - 14), (X0 + 2, Y0 - 6)], stroke=GRAY, sw=1)
s.line([(X0 + W - 2, Y0 - 14), (X0 + W - 2, Y0 - 6)], stroke=GRAY, sw=1)
s.text(CX, Y0 - 20, "d dimensions", size=12, color=GRAY, anchor="center", valign="bottom")

s.text(CX, Y0 + H + 12, "X: one embedded vector per row (n tokens x d)",
       size=13, color=BLUE, anchor="center")

s.save(os.path.join(OUT, "input-matrix.excalidraw"))
