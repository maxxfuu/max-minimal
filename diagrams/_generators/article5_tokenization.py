import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("tokenize")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

s.text(410, 8, "Tokenization: text becomes a list of integers", size=17, anchor="center")

WORDS = ["I", "love", "to", "study", "bats"]
IDS   = ["40", "1842", "284", "2050", "22526"]
WIDTH = [64, 96, 70, 112, 96]
GAP, X0, ROW_Y, ROW_H = 18, 155, 170, 52
total = sum(WIDTH) + GAP * (len(WORDS) - 1)
cx = X0 + total / 2

# ------------------------------------------------ gutter labels
for y, lab in ((86, "input text"), (196, "tokens"), (266, "token IDs")):
    s.text(130, y, lab, size=13, color=GRAY, anchor="right", valign="middle")

# ------------------------------------------------ the sentence
s.box(X0, 58, total, 56, '"I love to study bats"', size=20)
s.arrow([(cx, 124), (cx, 162)], stroke=GRAY)

# ------------------------------------------------ tokens and their IDs
x = X0
for w, i, tid in zip(WIDTH, WORDS, IDS):
    s.box(x, ROW_Y, w, ROW_H, i, size=18, stroke=BLUE, bg=BG_BLUE)
    s.text(x + w / 2, 266, tid, size=16, color=BLUE, anchor="center", valign="middle")
    x += w + GAP

s.text(cx, 318, "an ID is only an address in the vocabulary — it carries no meaning",
       size=13, color=GRAY, anchor="center")

s.save(os.path.join(OUT, "tokenization.excalidraw"))
