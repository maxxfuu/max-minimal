import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("singlehead")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

TOKENS = ["I", "love", "to", "study", "bats"]
N = len(TOKENS)
C = 18               # small cells: this figure shows shapes, not values
YELLOW = "#e67700"

s.text(440, 8, "Single-head attention, all of it at once", size=17, anchor="center")


def grid(x, y, cols, rows, stroke, bg, fill="solid", causal=False, label=None, tokens=False):
    for r in range(rows):
        if tokens:
            s.text(x - 8, y + r * C + C / 2, TOKENS[r], size=11, anchor="right", valign="middle")
        for c in range(cols):
            if causal and c > r:
                s.sq(x + c * C, y + r * C, C, C, stroke=GRAY, ss="dashed", sw=1)
            else:
                s.sq(x + c * C, y + r * C, C, C, stroke=stroke, bg=bg, fill=fill, sw=1)
    s.sq(x, y, cols * C, rows * C, stroke=stroke, sw=2)
    if causal:
        pts = [(x, y)]
        for i in range(rows):
            pts.append((x + (i + 1) * C, y + i * C))
            pts.append((x + (i + 1) * C, y + (i + 1) * C))
        s.line(pts, stroke=stroke, sw=2, roundness=SHARP)
    if label:
        s.text(x + cols * C / 2, y + rows * C + 6, label, size=12, color=stroke, anchor="center")
    return x + cols * C, y + rows * C / 2        # right edge, vertical centre


def step(p, q, text, dy=-8):
    s.arrow([p, q], stroke=GRAY, sw=1)
    s.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + dy, text, size=11, color=GRAY,
           anchor="center", valign="bottom")


# ------------------------------------------------ X -> Q, K, V
XR, XM = grid(70, 150, N, N, BLUE, BG_BLUE, label="X", tokens=True)
QY, KY, VY = 40, 150, 260
QR, QM = grid(230, QY, 3, N, RED, BG_RED, label="Q")
KR, KM = grid(230, KY, 3, N, GREEN, BG_GREEN, label="K")
VR, VM = grid(230, VY, 3, N, YELLOW, BG_YELLOW, label="V")
step((XR + 6, XM - 20), (224, QM + 20), "", dy=0)
step((XR + 6, XM), (224, KM), "W_K")
step((XR + 6, XM + 20), (224, VM - 20), "", dy=0)
s.text(XR + 2, XM - 50, "W_Q", size=11, color=GRAY, anchor="left", valign="bottom")
s.text(XR + 2, XM + 50, "W_V", size=11, color=GRAY, anchor="left", valign="top")

# ------------------------------------------------ Q, K -> S -> A
SX, SY = 360, 50
SR, SM = grid(SX, SY, N, N, VIOLET, BG_VIOLET, fill="hachure", causal=True, label="S = Q K^T")
step((QR + 6, QM), (SX - 6, SM - 24), "", dy=0)
step((KR + 6, KM), (SX - 6, SM + 24), "", dy=0)
AX = 500
AR, AM = grid(AX, SY, N, N, VIOLET, BG_VIOLET, fill="hachure", causal=True, label="A")
step((SR + 6, SM), (AX - 6, AM), "softmax")

# ------------------------------------------------ A, V -> O -> output
OX, OY = 640, 150
OR, OM = grid(OX, OY, 3, N, ORANGE_D, BG_ORANGE, label="O = A V")
step((AR + 6, AM), (OX - 6, OM - 20), "", dy=0)
step((VR + 6, VM), (OX - 6, OM + 20), "", dy=0)
UX = 740
grid(UX, OY, N, N, TEAL, BG_CYAN, fill="hachure", label="output")
step((OR + 6, OM), (UX - 6, OM), "W_O")

s.save(os.path.join(OUT, "single-head-overview.excalidraw"))
