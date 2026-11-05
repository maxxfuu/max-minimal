import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("dbuftime")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page13")

BL_ST, BL_BG = "#1971c2", "#a5d8ff"
LOAD, COMP, SYNC, LH = 90, 200, 12, 40    # widths in px, lane height

s.text(40, 12, "Double buffering  -  the K loop of one block, three tiles", size=24)
s.text(40, 48, "load = global memory into shared memory      compute = 16 dotIdx steps out of shared memory      | = __syncthreads()",
       size=13, color=GRAY)


def lanes(y, title):
    s.text(40, y - 26, title, size=15)
    s.text(150, y + LH / 2, "load pipe", size=12, color=GRAY_D, anchor="right", valign="middle")
    s.text(150, y + LH + 12 + LH / 2, "FMA pipe", size=12, color=GRAY_D, anchor="right", valign="middle")
    s.line([(164, y - 6), (164, y + 2 * LH + 18)], stroke=GRAY, sw=1, roundness=SHARP)
    return 170


def load_box(x, y, label, st=BL_ST, bg=BL_BG):
    s.sbox(x, y, LOAD, LH, label, size=12, stroke=st, bg=bg, fill="hachure", sw=2)


def comp_box(x, y, label):
    s.sbox(x, y, COMP, LH, label, size=12, stroke=GREEN, bg=BG_GREEN, fill="hachure", sw=2)


def sync(x, y):
    s.sq(x, y - 4, SYNC, 2 * LH + 20, stroke=GRAY_D, bg=GRAY_D, fill="solid", sw=1, opacity=35)


# ----------------------------------------------------------- kernel 10
Y1 = 120
x = lanes(Y1, "kernel 10   one buffer, two barriers per tile")
for n in range(3):
    load_box(x, Y1, "load %d" % n)
    x += LOAD
    sync(x, Y1); x += SYNC + 4
    comp_box(x, Y1 + LH + 12, "compute %d" % n)
    x += COMP
    sync(x, Y1); x += SYNC + 4
END1 = x
s.text(END1 + 10, Y1 + LH + 12 + LH / 2, "end", size=12, color=GRAY_D, valign="middle")
s.text(170, Y1 + 2 * LH + 26, "while loading, the FMA pipe is idle;  while computing, the load pipe is idle",
       size=12, color=GRAY_D)

# ----------------------------------------------------------- kernel 11
Y2 = 300
x = lanes(Y2, "kernel 11   two buffers, one barrier per tile")
# prologue
load_box(x, Y2, "load 0 → s0")
x += LOAD
sync(x, Y2); x += SYNC + 4
for n in range(3):
    if n + 1 < 3:
        load_box(x, Y2, "load %d → s%d" % (n + 1, (n + 1) % 2))
    comp_box(x, Y2 + LH + 12, "compute %d from s%d" % (n, n % 2))
    x += COMP
    sync(x, Y2); x += SYNC + 4
END2 = x
s.text(END2 + 10, Y2 + LH + 12 + LH / 2, "end", size=12, color=GRAY_D, valign="middle")
s.text(170, Y2 + 2 * LH + 26, "load n+1 runs underneath compute n;  the prologue load is paid once per block",
       size=12, color=GRAY_D)

# time axis
YA = Y2 + 2 * LH + 60
s.arrow([(170, YA), (END1 + 40, YA)], stroke=GRAY, sw=1)
s.text(170, YA + 8, "time", size=11, color=GRAY)
s.line([(END2, YA - 8), (END2, YA + 8)], stroke=GREEN, sw=2, roundness=SHARP)
s.line([(END1, YA - 8), (END1, YA + 8)], stroke=GRAY_D, sw=2, roundness=SHARP)

s.save(os.path.join(OUT, "double-buffer-timeline.excalidraw"))
