import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("tokenembed")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

s.text(400, 8, "Token Embedding: an ID becomes a vector of meaning", size=17, anchor="center")

# ------------------------------------------------ left: the lookup
s.box(20, 120, 104, 48, "bats", size=18, stroke=BLUE, bg=BG_BLUE)
s.text(72, 182, "22526", size=13, color=GRAY, anchor="center")

s.arrow([(134, 144), (202, 144)], stroke=GRAY)
s.text(168, 124, "lookup", size=12, color=GRAY, anchor="center", valign="bottom")

VALS = ["0.21", "-0.77", "0.05", "...", "-0.12", "0.63"]
for i, v in enumerate(VALS):
    s.box(210, 56 + i * 44, 100, 44, v, size=16, sw=1)

s.line([(324, 58), (324, 318)], stroke=GRAY, sw=1)
s.line([(324, 58), (332, 58)], stroke=GRAY, sw=1)
s.line([(324, 318), (332, 318)], stroke=GRAY, sw=1)
s.text(260, 336, "d dimensions (e.g. 768)", size=13, color=GRAY, anchor="center")

s.line([(400, 40), (400, 356)], stroke="#adb5bd", ss="dashed", sw=1)

# ------------------------------------------------ right: the embedding space
s.rect(410, 56, 382, 304, stroke=GRAY, sw=1)
s.text(424, 66, "embedding space (sketched in 2-D)", size=12, color=GRAY)

s.ellipse(436, 92, 150, 100, stroke=GREEN, ss="dashed", sw=1)
s.text(511, 200, "the animal", size=12, color=GREEN, anchor="center")

s.ellipse(626, 224, 150, 100, stroke=GREEN, ss="dashed", sw=1)
s.text(701, 332, "the baseball bat", size=12, color=GREEN, anchor="center")

NEIGHBOURS = [(470, 128, "cave"), (528, 140, "wings"), (496, 172, "nocturnal"),
              (676, 268, "pitch"), (730, 278, "glove"), (700, 306, "swing")]
for x, y, lab in NEIGHBOURS:
    s.ellipse(x - 5, y - 5, 10, 10, stroke=BLACK, bg=BLACK, sw=1)
    s.text(x, y - 12, lab, size=13, anchor="center", valign="bottom")

# the ambiguous token: one point, pulled toward both senses
s.ellipse(598, 200, 16, 16, stroke=RED, bg=BG_RED, sw=2)
s.text(622, 208, "bats", size=16, color=RED, valign="middle")
s.arrow([(598, 204), (562, 178)], stroke=RED, ss="dashed", sw=1)
s.arrow([(614, 218), (648, 244)], stroke=RED, ss="dashed", sw=1)

s.text(400, 374, "one token gets one fixed vector — the sentence it sits in cannot change it",
       size=13, color=GRAY, anchor="center")

s.save(os.path.join(OUT, "token-embedding.excalidraw"))
