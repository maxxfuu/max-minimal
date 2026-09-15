import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("attnarch")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "article5")

PANEL_BG = "#f8f9fa"
ANNOT = BLUE

def stack(fn, n=2, dx=7, dy=-7):
    """Draw n faded copies behind a shape to say 'h of these, in parallel'."""
    for i in range(n, 0, -1):
        fn(i * dx, i * dy, {"opacity": 40})
    fn(0, 0, {})

def wave(cx, cy, w=30, h=7):
    pts = [(cx - w / 2 + i, cy - h * math.sin(i / w * 2 * math.pi)) for i in range(0, w + 1, 2)]
    s.line(pts, sw=1)

# ================================================================ left: the transformer
s.text(300, 104, "The Transformer", size=17, anchor="center")
s.text(300, 128, "encoder on the left, decoder on the right", size=12, color=GRAY, anchor="center")

XE, XD, BW = 190, 420, 150          # column centres, box width
enc_l, dec_l = XE - BW / 2, XD - BW / 2

# -- the two residual stacks ------------------------------------------------
s.rect(90, 398, 200, 208, stroke=GRAY, bg=PANEL_BG, sw=1)
s.rect(320, 302, 200, 304, stroke=GRAY, bg=PANEL_BG, sw=1)

def sub(x, y, h, label, bg, size=13):
    return s.box(x, y, BW, h, label, size=size, bg=bg, sw=1)

# encoder: attention -> add&norm -> feed forward -> add&norm
sub(enc_l, 548, 44, "Multi-Head\nAttention", BG_ORANGE)
sub(enc_l, 506, 30, "Add & Norm", BG_YELLOW, size=12)
sub(enc_l, 452, 44, "Feed\nForward", BG_BLUE)
sub(enc_l, 410, 30, "Add & Norm", BG_YELLOW, size=12)

# decoder: masked attention -> cross attention -> feed forward
sub(dec_l, 548, 44, "Masked\nMulti-Head Attention", BG_ORANGE, size=12)
sub(dec_l, 506, 30, "Add & Norm", BG_YELLOW, size=12)
sub(dec_l, 452, 44, "Multi-Head\nAttention", BG_ORANGE)
sub(dec_l, 410, 30, "Add & Norm", BG_YELLOW, size=12)
sub(dec_l, 356, 44, "Feed\nForward", BG_BLUE)
sub(dec_l, 314, 30, "Add & Norm", BG_YELLOW, size=12)

# -- vertical flow inside each stack ---------------------------------------
for x, pairs in ((XE, [(548, 538), (506, 498), (452, 442)]),
                 (XD, [(548, 538), (506, 498), (452, 442), (410, 402), (356, 346)])):
    for y0, y1 in pairs:
        s.arrow([(x, y0), (x, y1)], sw=1)

# -- the residual connections, routed around the left of each stack ---------
def residual(x_edge, x_trunk, x_box, y_from, y_to):
    """Branch off the trunk below a sublayer, round the outside, into Add & Norm."""
    s.arrow([(x_trunk, y_from), (x_edge, y_from), (x_edge, y_to), (x_box, y_to)], sw=1)

residual(102, XE, enc_l, 600, 521)
residual(102, XE, enc_l, 501, 425)
residual(332, XD, dec_l, 600, 521)
residual(332, XD, dec_l, 501, 425)
residual(332, XD, dec_l, 405, 329)

# -- Q, K, V fan-out into the two self-attention blocks --------------------
def fan(cx, y_line, y_box):
    s.line([(cx - 38, y_line), (cx + 38, y_line)], sw=1)
    for dx in (-38, 0, 38):
        s.arrow([(cx + dx, y_line), (cx + dx, y_box)], sw=1)

fan(XE, 624, 592)
fan(XD, 624, 592)

# -- embeddings, positional encoding, inputs -------------------------------
for x, label in ((XE, "Input\nEmbedding"), (XD, "Output\nEmbedding")):
    s.box(x - BW / 2, 700, BW, 44, label, size=13, bg=BG_RED, sw=1)
    plus = s.ellipse(x - 13, 637, 26, 26, sw=1)
    s.label(plus, "+", size=16)
    s.arrow([(x, 700), (x, 665)], sw=1)
    s.line([(x, 637), (x, 624)], sw=1)

wave(140, 650)
s.arrow([(156, 650), (176, 650)], sw=1)
s.text(118, 650, "Positional\nEncoding", size=12, anchor="right", valign="middle")

wave(470, 650)
s.arrow([(454, 650), (434, 650)], sw=1)
s.text(492, 650, "Positional\nEncoding", size=12, valign="middle")

s.text(XE, 800, "Inputs", size=14, anchor="center")
s.arrow([(XE, 790), (XE, 746)], sw=1)
s.text(XD, 800, "Outputs\n(shifted right)", size=14, anchor="center")
s.arrow([(XD, 790), (XD, 746)], sw=1)

# -- encoder output feeding K and V into cross attention -------------------
s.line([(XE, 410), (XE, 372), (306, 372)], sw=1)
s.arrow([(292, 372), (292, 462), (dec_l, 462)], sw=1)
s.arrow([(306, 372), (306, 486), (dec_l, 486)], sw=1)
s.text(299, 362, "K, V", size=12, color=GRAY, anchor="center", valign="bottom")

# -- the head of the model -------------------------------------------------
s.arrow([(XD, 314), (XD, 298)], sw=1)
s.box(dec_l, 252, BW, 44, "Linear", size=14, bg=BG_VIOLET, sw=1)
s.arrow([(XD, 252), (XD, 240)], sw=1)
s.box(dec_l, 192, BW, 44, "Softmax", size=14, bg=BG_GREEN, sw=1)
s.arrow([(XD, 192), (XD, 186)], sw=1)
s.text(XD, 182, "Output\nProbabilities", size=14, anchor="center", valign="bottom")

s.text(78, 502, "N×", size=15, anchor="right", valign="middle")
s.text(532, 340, "N×", size=15, valign="middle")

# -- the two annotations from the reference figure -------------------------
s.arrow([(542, 470), (499, 470)], stroke=ANNOT, sw=1)
s.text(548, 470, "Cross Attention", size=13, color=ANNOT, valign="middle")
s.arrow([(542, 570), (499, 570)], stroke=ANNOT, sw=1)
s.text(548, 570, "Masked Multi-Head\nAttention", size=13, color=ANNOT, valign="middle")

s.line([(630, 100), (630, 860)], stroke="#adb5bd", ss="dashed", sw=1)

# ================================================================ right: multi-head attention
XM = 900
s.text(XM, 104, "Multi-Head Attention", size=17, anchor="center")
s.text(XM, 128, "one attention head, run h times in parallel", size=12, color=GRAY, anchor="center")

for x, lab in ((820, "V"), (900, "K"), (980, "Q")):
    s.text(x, 776, lab, size=16, anchor="center")
    s.arrow([(x, 766), (x, 730)], sw=1)
    stack(lambda dx, dy, kw, x=x: s.box(x - 32 + dx, 686 + dy, 64, 40, "Linear", size=13,
                                        bg=BG_VIOLET, sw=1, **kw))
    s.arrow([(x, 686), (x, 644)], sw=1)

stack(lambda dx, dy, kw: s.box(770 + dx, 572 + dy, 260, 72, "Scaled Dot-Product\nAttention",
                               size=15, bg=BG_ORANGE, sw=1, **kw))

s.arrow([(XM, 572), (XM, 524)], sw=1)
s.box(790, 480, 220, 44, "Concat", size=15, bg=BG_YELLOW, sw=1)
s.arrow([(XM, 480), (XM, 436)], sw=1)
s.box(830, 392, 140, 44, "Linear", size=15, bg=BG_VIOLET, sw=1)
s.arrow([(XM, 392), (XM, 352)], sw=1)
s.text(XM, 348, "MultiHead(Q, K, V)", size=15, anchor="center", valign="bottom")

s.arrow([(1062, 556), (1046, 576)], stroke=GRAY, sw=1)
s.text(1068, 550, "h heads, each with\nits own projections", size=12, color=GRAY, valign="middle")

s.text(XM, 820, "Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V",
       size=13, font=CODE, anchor="center")
s.text(XM, 846, "head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)",
       size=13, font=CODE, anchor="center")

# ---------------------------------------------------------------- saving
# This figure was edited by hand in the Excalidraw app after it was generated:
# the dashed frame that marks the right panel as a zoom into cross attention,
# the pointer into it, and the removal of the callout labels it replaced. The
# scene file is the source of truth from here on, so a plain rebuild refuses to
# overwrite it. Run with FORCE=1 to regenerate from scratch and lose those edits.
target = os.path.join(OUT, "attention-architecture.excalidraw")

if os.path.exists(target) and not os.environ.get("FORCE"):
    import json
    handmade = [e for e in json.load(open(target))["elements"]
                if not e["id"].startswith("attnarch-")]
    if handmade:
        # exit clean, build_all.sh runs under `set -e`
        print("skipping %s: %d hand-drawn element(s) present, FORCE=1 to overwrite"
              % (os.path.basename(target), len(handmade)))
        raise SystemExit(0)

s.save(target)
