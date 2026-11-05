import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("retune")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page14")

CY_ST, CY_BG = "#0c8599", "#99e9f2"
BL_ST, BL_BG = "#1971c2", "#a5d8ff"
C = 14   # px per accumulator

s.text(40, 12, "Retuning the thread tile  -  what one thread does per dotIdx", size=24)
s.text(40, 48, "loads from shared memory into regM and regN, then every pairwise product into the accumulators",
       size=13, color=GRAY)


def panel(x0, y0, title, nA, nB, sub, note):
    # matmul layout: regM (column of A values) bottom-left, regN (row of B values) top-right,
    # accumulators bottom-right
    s.text(x0, y0, title, size=15)
    ax, ay = x0 + 20, y0 + 40 + C + 16
    bx, by = ax + C + 16, y0 + 40
    # regN row
    grid_box(s, bx, by, nB * C, C, nB, 1, stroke=CY_ST, sw=2, bg=CY_BG)
    s.text(bx + nB * C + 10, by + C / 2, "regN  %d" % nB, size=12, color=CY_ST, valign="middle")
    # regM column
    grid_box(s, ax, ay, C, nA * C, 1, nA, stroke=BL_ST, sw=2, bg=BL_BG)
    s.text(ax - 8, ay + nA * C / 2, "regM\n%d" % nA, size=12, color=BL_ST, anchor="right", valign="middle",
           align="right")
    # accumulators
    grid_box(s, bx, ay, nB * C, nA * C, nB, nA, stroke=GREEN, sw=2, bg=BG_GREEN, fill="hachure")
    s.text(bx + nB * C + 10, ay + nA * C / 2, "%d accumulators" % (nA * nB), size=12, color=GREEN, valign="middle")
    yb = ay + nA * C + 16
    s.text(ax, yb, sub, size=13)
    s.text(ax, yb + 22, note, size=12, color=GRAY_D)
    return yb + 48


# kernel 11: WMITER x TM = 2 x 4 = 8 values of A, WNITER x TN = 2 x 4 = 8 of B, 64 accumulators
panel(40, 100, "kernel 11   T4x4, WMITER = 2, WNITER = 2",
      8, 8, "8 + 8 = 16 loads  →  64 FMAs   ·   4.0 FMA per float loaded",
      "eight LDS.32 from As (4 + 4, two sub-tiles)   ·   150 registers, 3 blocks per SM")

# kernel 12: WMITER x TM = 1 x 16 = 16 values of A, WNITER x TN = 2 x 4 = 8 of B, 128 accumulators
panel(520, 100, "kernel 12   T16x4, WMITER = 1, WNITER = 2",
      16, 8, "16 + 8 = 24 loads  →  128 FMAs   ·   5.3 FMA per float loaded",
      "four LDS.128 from As (16 contiguous)   ·   227 registers, 2 blocks per SM")

s.save(os.path.join(OUT, "thread-tile-retune.excalidraw"))
