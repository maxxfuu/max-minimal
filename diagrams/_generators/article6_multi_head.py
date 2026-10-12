import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("multihead")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

TOKENS = ["I", "love", "to", "study", "bats"]
N = len(TOKENS)
D, H = 8, 4          # embedding width and number of heads shown; each head gets D / H
DH = D // H
C = 16               # small cells: shapes, not values
YELLOW = "#e67700"



def grid(x, y, cols, rows, stroke, bg, fill="solid", causal=False, sw=1, tokens=False, divide=0):
    for r in range(rows):
        if tokens:
            s.text(x - 8, y + r * C + C / 2, TOKENS[r], size=10, anchor="right", valign="middle")
        for c in range(cols):
            if causal and c > r:
                s.sq(x + c * C, y + r * C, C, C, stroke=GRAY, ss="dashed", sw=1)
            else:
                s.sq(x + c * C, y + r * C, C, C, stroke=stroke, bg=bg, fill=fill, sw=sw)
    if divide:   # heavier lines between the per-head slices of a concatenated block
        for c in range(divide, cols, divide):
            s.line([(x + c * C, y), (x + c * C, y + rows * C)], stroke=stroke, sw=2, roundness=SHARP)
    s.sq(x, y, cols * C, rows * C, stroke=stroke, sw=2)
    if causal:
        pts = [(x, y)]
        for i in range(rows):
            pts.append((x + (i + 1) * C, y + i * C))
            pts.append((x + (i + 1) * C, y + (i + 1) * C))
        s.line(pts, stroke=stroke, sw=2, roundness=SHARP)
    return x + cols * C, y + rows * C / 2


def arrow(p, q, text=None, dy=-6):
    s.arrow([p, q], stroke=GRAY, sw=1)
    if text:
        s.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + dy, text, size=10, color=GRAY,
               anchor="center", valign="bottom")


# ------------------------------------------------ horizontal layout, left to right
PX, PY, PH = 40, 76, 440
XX = PX + 60
QX = XX + D * C + 116
KX = QX + DH * C + 8
VX = KX + DH * C + 8
SX = VX + DH * C + 28
AX = SX + N * C + 36
OX = AX + N * C + 28
CX = OX + DH * C + 50
UX = CX + D * C + 60
PW = UX + D * C + 30 - PX

s.text(PX + PW / 2, 8, "Multi-head attention: 4 heads in a layer, 3 layers stacked", size=17, anchor="center")

# ------------------------------------------------ the layer panel, with the layers behind it
for i in (2, 1):                          # layers 2..N, offset up and to the right
    s.rect(PX + 14 * i, PY - 14 * i, PW, PH, stroke=BLACK, bg="#ffffff", ss="dotted", sw=1)
s.rect(PX, PY, PW, PH, stroke=GRAY_D, bg="#ffffff", sw=2)
s.text(PX + PW + 14 * 2 + 8, PY - 14 * 2 + 10, "layers 2, 3", size=13, anchor="left")

ROW = N * C + 14                          # height of one head's row
Y0 = PY + 40                              # top of head 1
MID = Y0 + (H * ROW - 18) / 2             # vertical centre of the head stack

# ------------------------------------------------ X, shared by every head
XR, XM = grid(XX, MID - N * C / 2, D, N, BLUE, BG_BLUE, tokens=True)
s.text(XX + D * C / 2, MID + N * C / 2 + 6, "X  (n x d)", size=11, color=BLUE, anchor="center")

# ------------------------------------------------ h heads, each the single-head mechanism on a d/h slice
for lab, x in (("Q", QX), ("K", KX), ("V", VX), ("S", SX + N * C / 2 - C / 2), ("A", AX + N * C / 2 - C / 2), ("O", OX)):
    s.text(x + DH * C / 2, Y0 - 8, lab, size=11, color=GRAY, anchor="center", valign="bottom")
for h in range(H):
    y = Y0 + h * ROW
    m = y + N * C / 2
    s.text(QX - 12, m, "head %d" % (h + 1), size=11, anchor="right", valign="middle")
    arrow((XR + 6, XM + (h - (H - 1) / 2) * 10), (QX - 72, m))
    grid(QX, y, DH, N, RED, BG_RED)
    grid(KX, y, DH, N, GREEN, BG_GREEN)
    grid(VX, y, DH, N, YELLOW, BG_YELLOW)
    grid(SX, y, N, N, VIOLET, BG_VIOLET, fill="hachure", causal=True)
    grid(AX, y, N, N, VIOLET, BG_VIOLET, fill="hachure", causal=True)
    arrow((SX + N * C + 6, m), (AX - 6, m))
    OR, _ = grid(OX, y, DH, N, ORANGE_D, BG_ORANGE)
    arrow((AX + N * C + 6, m), (OX - 6, m))

# ------------------------------------------------ concat the h outputs, then W_O
CR, CM = grid(CX, MID - N * C / 2, D, N, ORANGE_D, BG_ORANGE, divide=DH)
s.text(CX + D * C / 2, MID + N * C / 2 + 6, "concat  (n x d)", size=11, color=ORANGE_D, anchor="center")
for h in range(H):
    m = Y0 + h * ROW + N * C / 2
    arrow((OX + DH * C + 6, m), (CX - 6, CM + (h - (H - 1) / 2) * 12))

grid(UX, MID - N * C / 2, D, N, TEAL, BG_CYAN, fill="hachure")
s.text(UX + D * C / 2, MID + N * C / 2 + 6, "output  (n x d)", size=11, color=TEAL, anchor="center")
arrow((CR + 6, CM), (UX - 6, CM), "W_O")

s.save(os.path.join(OUT, "multi-head.excalidraw"))
