import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exc import *

s = Scene("autosweep")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "page11")

# config, ms (from page11's table, autotuner harness)
rows = [
    ("128x64x16   W64x32    I2  T4x4  128t", 4.55),
    ("128x128x16  W64x64    I4  T8x4  128t", 4.66),
    ("128x128x16  W64x64    I2  T8x8  128t", 4.67),
    ("128x128x16  W64x64    I4  T4x8  128t", 4.76),
    ("64x128x16   W32x64    I4  T4x4  128t", 4.90),
    ("128x128x32  W64x64    I4  T8x4  128t", 4.91),
    ("128x128x8   W64x64    I4  T8x4  128t", 5.00),
    ("256x64x16   W64x32    I2  T8x4  256t", 5.02),
    ("128x128x16  W32x64    I2  T4x4  256t", 5.05),
    ("128x256x16  W64x64    I4  T8x4  256t", 5.27),
    ("128x128x8   W32x64    I2  T4x4  256t", 5.33),
    ("256x128x16  W128x32   I2  T8x4  256t", 5.47),
    ("64x64x16    W32x32    I2  T4x4  128t", 5.72),
    ("256x128x16  W64x32    I2  T8x4  512t", 6.17),
]

s.text(40, 12, "Autotuning  -  the 14 legal configurations, ranked by runtime", size=24)
s.text(40, 48, "BM x BN x BK   W = WM x WN   I = WNITER   T = TM x TN   threads per block   ·   M = N = K = 4096",
       size=13, color=GRAY)

X0, Y0, RH, PX = 400, 100, 26, 70     # bar origin, row height, px per ms
for i, (cfg, ms) in enumerate(rows):
    y = Y0 + i * RH
    win = i == 0
    s.text(X0 - 14, y + RH / 2, cfg, size=12, font=CODE, anchor="right", valign="middle",
           color=GREEN if win else GRAY_D)
    s.sq(X0, y + 4, ms * PX, RH - 8, stroke=GREEN if win else GRAY, bg=BG_GREEN if win else BG_GRAY,
         fill="hachure" if win else "solid", sw=2 if win else 1)
    s.text(X0 + ms * PX + 8, y + RH / 2, "%.2f ms" % ms, size=12, valign="middle",
           color=GREEN if win else GRAY_D)

# the two configs cfg_valid() rejected
yi = Y0 + len(rows) * RH + 6
for k in range(2):
    y = yi + k * RH
    s.sq(X0, y + 4, 60, RH - 8, stroke=GRAY, ss="dashed", sw=1)
s.text(X0 - 14, yi + RH, "2 configs", size=12, font=CODE, anchor="right", valign="middle", color=GRAY)
s.text(X0 + 72, yi + RH, "skipped: illegal shape, rejected by cfg_valid() at compile time",
       size=12, valign="middle", color=GRAY)

# axis
ya = yi + 2 * RH + 14
s.line([(X0, ya), (X0 + 6.5 * PX, ya)], stroke=GRAY, sw=1, roundness=SHARP)
for t in range(0, 7):
    s.line([(X0 + t * PX, ya), (X0 + t * PX, ya + 6)], stroke=GRAY, sw=1, roundness=SHARP)
    s.text(X0 + t * PX, ya + 10, str(t), size=11, color=GRAY, anchor="center")
s.text(X0 + 6.5 * PX + 10, ya - 2, "ms", size=11, color=GRAY, valign="middle")

# callouts
s.text(X0 + 6.5 * PX + 40, Y0 + 10, "winner: 128 × 64, 4 × 4, 128 threads", size=12, color=GREEN)
s.text(X0 + 6.5 * PX + 40, Y0 + 30, "2.4% ahead of the best square tile", size=12, color=GRAY_D)
s.text(X0 + 6.5 * PX + 40, Y0 + 13 * RH + 10, "slowest legal: 1 block per SM", size=12, color=GRAY_D)
s.text(X0 + 6.5 * PX + 40, Y0 + 13 * RH + 30, "best to worst = 1.36 times", size=12, color=GRAY_D)

s.save(os.path.join(OUT, "autotune-sweep.excalidraw"))
