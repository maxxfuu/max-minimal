import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("attnscores")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article6")

TOKENS = ["I", "love", "to", "study", "bats"]
C = 44            # cell size, every matrix shares it
CX = 385

s.text(CX, 8, "Scoring every token against every other token: S = Q K^T", size=17, anchor="center")

# the pair of tokens we follow through the product
I, J = 1, 4       # love -> bats

# Laid out like a matmul on paper: K^T top right, Q bottom left, S bottom right,
# so S shares its rows with Q and its columns with K^T.

# ------------------------------------------------ K^T : d_k x n, one key column per token
KT = [
    ["0.2", "-0.4", "0.9", "0.5", "1.2"],
    ["0.7", "0.3", "-0.1", "-0.6", "0.8"],
    ["-0.3", "1.0", "0.4", "0.2", "-0.5"],
    ["...", "...", "...", "...", "..."],
]
KX, KY = 330, 72
KW, KH = C * len(KT[0]), C * len(KT)
for c, tok in enumerate(TOKENS):
    s.text(KX + c * C + C / 2, KY - 8, tok, size=14, anchor="center", valign="bottom")
for r, row in enumerate(KT):
    for c, v in enumerate(row):
        s.sbox(KX + c * C, KY + r * C, C, C, v, size=13, stroke=GREEN, bg=BG_GREEN, sw=1)
s.sq(KX, KY, KW, KH, stroke=GREEN, sw=2)
s.sq(KX + J * C, KY, C, KH, stroke=GREEN, sw=3)                       # k_bats
s.text(KX + KW + 14, KY + KH / 2, "K^T  (d_k x n)", size=13, color=GREEN, valign="middle")

# ------------------------------------------------ Q : n x d_k, one query row per token
Q = [
    ["0.8", "-0.3", "1.1", "..."],
    ["1.4", "0.9", "-0.2", "..."],
    ["-0.5", "0.2", "0.4", "..."],
    ["0.3", "-1.0", "0.7", "..."],
    ["0.6", "0.1", "-0.8", "..."],
]
QW, QH = C * len(Q[0]), C * len(Q)
QX, QY = KX - 44 - QW, KY + KH + 40
for r, (tok, row) in enumerate(zip(TOKENS, Q)):
    y = QY + r * C
    s.text(QX - 12, y + C / 2, tok, size=14, anchor="right", valign="middle")
    for c, v in enumerate(row):
        s.sbox(QX + c * C, y, C, C, v, size=13, stroke=RED, bg=BG_RED, sw=1)
s.sq(QX, QY, QW, QH, stroke=RED, sw=2)
s.sq(QX, QY + I * C, QW, C, stroke=RED, sw=3)                         # q_love
s.text(QX + QW / 2, QY + QH + 8, "Q  (n x d_k)", size=13, color=RED, anchor="center")

# ------------------------------------------------ S : n x n raw scores, row i attends to column j
S = [
    ["1.9", "0.6", "-0.2", "0.8", "1.1"],
    ["0.5", "2.3", "0.1", "-0.4", "2.7"],
    ["-0.3", "0.2", "1.5", "0.9", "0.0"],
    ["0.7", "-0.6", "1.0", "2.1", "0.3"],
    ["1.2", "0.4", "-0.1", "0.6", "1.8"],
]
SX, SY = KX, QY
SW, SH = C * len(S[0]), C * len(S)
for r, row in enumerate(S):
    for c, v in enumerate(row):
        s.sbox(SX + c * C, SY + r * C, C, C, v, size=13, stroke=VIOLET, bg=BG_VIOLET,
               fill="hachure", sw=1)
s.sq(SX, SY, SW, SH, stroke=VIOLET, sw=2)
s.sq(SX + J * C, SY + I * C, C, C, stroke=VIOLET, sw=3)               # S[love, bats]
s.text(SX + SW / 2, SY + SH + 8, "S = Q K^T  (n x n)", size=13, color=VIOLET, anchor="center")

# ------------------------------------------------ the pair, read off the two highlighted cells
BY = SY + SH + 44
s.text(CX, BY, "S[love, bats] = q_love . k_bats = 2.7      S[bats, love] = q_bats . k_love = 0.4",
       size=14, anchor="center")

s.save(os.path.join(OUT, "attention-scores.excalidraw"))
