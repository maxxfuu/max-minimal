import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("nexttoken")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

TOKENS = ["I", "love", "to", "study", "bats"]
VOCAB = ["that", "in", ".", "and", "cats", "..."]
N, D, VN = len(TOKENS), 5, len(VOCAB)
C = 32



def grid(x, y, cols, rows, stroke, bg, fill="solid", tokens=False):
    for r in range(rows):
        if tokens:
            s.text(x - 10, y + r * C + C / 2, TOKENS[r], size=12, anchor="right", valign="middle")
        for c in range(cols):
            s.sq(x + c * C, y + r * C, C, C, stroke=stroke, bg=bg, fill=fill, sw=1)
    s.sq(x, y, cols * C, rows * C, stroke=stroke, sw=2)


# ------------------------------------------------ X^(N): the stack's output, last row outlined
XX, XY = 70, 70
grid(XX, XY, D, N, BLUE, BG_BLUE, tokens=True)
s.sq(XX, XY + (N - 1) * C, D * C, C, stroke=BLUE, sw=3)
s.text(XX + D * C / 2, XY + N * C + 8, "X^(N)  (n x d)", size=13, color=BLUE, anchor="center")

# ------------------------------------------------ last row x W_vocab = logits, laid out as a matmul
RX = XX + D * C + 70                            # x_n sits to the right of X^(N)
WX, WY = RX + D * C + 24, XY                    # W_vocab top-right
grid(WX, WY, VN, D, GRAY_D, BG_GRAY)
s.text(WX + VN * C / 2, WY + D * C + 8, "W_vocab  (d x |V|)", size=13, color=GRAY_D, anchor="center")
RY = WY + D * C + 44                            # bottom row: x_n and the logits
grid(RX, RY, D, 1, BLUE, BG_BLUE)
s.text(RX + D * C / 2, RY + C + 8, "x_n  (1 x d)", size=13, color=BLUE, anchor="center")
grid(WX, RY, VN, 1, GRAY_D, BG_GRAY, fill="hachure")
s.text(WX + VN * C / 2, RY + C + 8, "logits  (1 x |V|)", size=13, color=GRAY_D, anchor="center")
s.arrow([(XX + D * C + 8, XY + (N - 0.5) * C), (RX - 8, RY + C / 2)], stroke=GRAY, sw=1)
s.text((XX + D * C + RX) / 2, XY + (N - 0.5) * C - 6, "last row", size=11, color=GRAY,
       anchor="center", valign="bottom")

# ------------------------------------------------ softmax over the vocabulary: a bar per word
BX = WX + VN * C + 70
BW, BH = 26, 150
BY = RY + C - BH + C / 2                        # bars bottom-aligned with the logits row
probs = [0.46, 0.20, 0.13, 0.09, 0.06, 0.06]
s.arrow([(WX + VN * C + 8, RY + C / 2), (BX - 12, RY + C / 2)], stroke=GRAY, sw=1)
s.text((WX + VN * C + BX) / 2, RY + C / 2 - 6, "softmax", size=11, color=GRAY, anchor="center", valign="bottom")
s.line([(BX - 4, BY + BH), (BX + VN * (BW + 10), BY + BH)], stroke=BLACK, sw=1)
for i, (w, p) in enumerate(zip(VOCAB, probs)):
    x = BX + i * (BW + 10)
    h = BH * p / max(probs)
    s.sq(x, BY + BH - h, BW, h, stroke=TEAL, bg=BG_CYAN, sw=1)
    s.text(x + BW / 2, BY + BH - h - 4, "%.2f" % p, size=10, anchor="center", valign="bottom")
    s.text(x + BW / 2, BY + BH + 8, w, size=12, anchor="center")
s.text(BX + VN * (BW + 10) / 2 - 5, BY + BH + 30, "p(next token)  sums to 1", size=13, color=TEAL, anchor="center")

# title, centred over the full width of the figure
s.text((XX + BX + VN * (BW + 10)) / 2, 8, "The last row becomes a distribution over the vocabulary", size=17, anchor="center")

s.save(os.path.join(OUT, "next-token.excalidraw"))
