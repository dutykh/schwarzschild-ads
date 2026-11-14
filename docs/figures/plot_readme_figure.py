#!/usr/bin/env python3
# Dr. Denys Dutykh (Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, UAE)
"""Figure of the README: scalar quasinormal modes of Schwarzschild-anti-de Sitter black holes with the
vanishing-field condition at the AdS boundary, read from reports/s0-vanishing-AdS-boundary/.

From this folder,
    python3 plot_readme_figure.py
writes schwarzschild-ads-modes.png. Panel (a): real part and damping rate of the least damped l = 0 mode
against the horizon radius x+ = r+/R, with the pure-AdS value 3 and the large-black-hole slopes 1.85 and
2.66 quoted by the article. Panel (b): the overtones of l = 0, 1, 2, 3 at x+ = 0.4
with Re Omega <= 20 and Im Omega >= -12. The value of x+ is read
from the file tag (a = 1000 x+), which is right in every report. The style is the stamped copy
manuscript_style.py beside this script.
"""
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent.parent / "reports" / "s0-vanishing-AdS-boundary"
sys.path.insert(0, str(HERE))
import manuscript_style as hs  # noqa: E402


def read_report(path):
    """Horizon radius from the tag of the file name, and the tabulated roots."""
    text = path.read_text()
    tag = re.search(r"File tag: (\S+)", text).group(1)
    over = re.search(r"xp(\d+)over(\d+)", tag)
    x_plus = int(over.group(1)) / int(over.group(2)) if over else int(re.search(r"_a(\d+)", tag).group(1)) / 1000
    roots = [complex(float(p[1]), float(p[2])) for p in (line.split() for line in text.splitlines())
             if len(p) == 7 and p[0].isdigit()]
    return x_plus, np.array(roots)


points = []
for path in sorted((REPORTS / "L0").glob("*.txt")):
    x_plus, roots = read_report(path)
    oscillatory = roots[roots.real > 0]
    points.append((x_plus, oscillatory[np.argmax(oscillatory.imag)]))
points.sort(key=lambda p: p[0])
x_plus = np.array([p[0] for p in points])
omega = np.array([p[1] for p in points])

hs.configure(family="libertine")
plt.rcParams["savefig.dpi"] = 265
plt.rcParams["figure.facecolor"] = hs.PAPER
plt.rcParams["savefig.facecolor"] = hs.PAPER

fig, (ax_x, ax_sp) = plt.subplots(1, 2, figsize=(hs.WIDTH, 2.7), gridspec_kw={"width_ratios": [1.15, 1]})
guide = dict(color=hs.SLATE, lw=0.7, linestyle=(0, (1.6, 1.6)), zorder=0)
large = np.array([1.0, 150.0])
ax_x.plot([0.03, 150.0], [3.0, 3.0], **guide)
ax_x.plot(large, 1.85 * large, **guide)
ax_x.plot(large, 2.66 * large, **guide)
real_style, damp_style = hs.series(0), hs.series(1)
for style in (real_style, damp_style):
    style["markersize"] = 3.0
ax_x.loglog(x_plus, omega.real, lw=0.9, label=r"$\mathrm{Re}\,\Omega$, least damped mode, $\ell = 0$", **real_style)
ax_x.loglog(x_plus, -omega.imag, lw=0.9, label=r"$-\mathrm{Im}\,\Omega$, least damped mode, $\ell = 0$", **damp_style)
ax_x.set_xlim(0.03, 150.0)
ax_x.set_ylim(5e-3, 600.0)
ax_x.set_xlabel(r"$x_+ = r_+ / R$")
ax_x.set_ylabel(r"$\Omega = \omega R$")
hs.grid(ax_x)
hs.panel(ax_x, "(a) least damped mode against the horizon radius")

for ell in range(4):
    name = f"s0_L{ell}_xp0_4.txt"
    _, roots = read_report(REPORTS / f"L{ell}" / name)
    roots = roots[(roots.real > 0) & (roots.real <= 20.0) & (roots.imag >= -12.0)]
    style = hs.series(ell + 2)
    ax_sp.plot(roots.real, roots.imag, linestyle="none", marker=style["marker"], markersize=2.6,
               markerfacecolor="white", markeredgecolor=style["color"], markeredgewidth=0.8,
               label=rf"$\ell = {ell}$, $x_+ = 0.4$")
ax_sp.set_xlim(0.0, 21.0)
ax_sp.set_ylim(-12.8, 0.0)
ax_sp.set_xlabel(r"$\mathrm{Re}\,\Omega$")
ax_sp.set_ylabel(r"$\mathrm{Im}\,\Omega$")
hs.panel(ax_sp, "(b) overtones")

hs.legend_outside(fig, where="upper", ncol=3)
out = HERE / "schwarzschild-ads-modes.png"
hs.save(fig, out)
print("written", out)
