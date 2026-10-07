"""Reproduce both ChickWeight figures under the figure-contract rules.

    python make_figures.py

Reads data/chickweight.csv (exported from R's datasets::ChickWeight) and writes
figures/fig1_growth_trajectories.png and figures/fig2_final_measurement.png.
Each figure is checked with audit_figure() from skill/kernel.py before saving;
the script exits non-zero if either figure has an unresolved violation.

Questions the figures answer:
  Q1  How do growth trajectories differ across diets, and how consistent are
      those patterns across individual chicks?
  Q2  What changes if we compare only the final measurement?
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "skill"))
from kernel import audit_figure, panel_name  # noqa: E402

# One colour per diet, identical in both figures (same group -> same colour).
PAL = {1: "#0072B2", 2: "#E69F00", 3: "#009E73", 4: "#CC79A7"}
BACK, OWN = "0.86", "0.50"


def style():
    """Role-mapped font ladder, outward ticks, no top/right spines, 300 dpi."""
    plt.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 300, "savefig.bbox": "tight",
        "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
        "legend.fontsize": 7, "xtick.labelsize": 6, "ytick.labelsize": 6,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.direction": "out", "ytick.direction": "out",
        "axes.titlelocation": "left", "legend.frameon": False,
        "lines.solid_capstyle": "round",
    })


def panel_letter(ax, letter):
    ax.annotate(letter, xy=(-0.14, 1.06), xycoords="axes fraction",
                fontsize=10, fontweight="bold", va="bottom", ha="left")


def load():
    d = pd.read_csv(os.path.join(HERE, "data", "chickweight.csv"))
    d["Chick"] = d["Chick"].astype(int)
    d["Diet"] = d["Diet"].astype(int)
    return d.sort_values(["Chick", "Time"])


def cohort(d):
    """Enrolment, retention and the chicks that left before day 21."""
    last = d.groupby("Chick").last()
    enrolled = d.groupby("Chick").first().groupby("Diet").size()
    at21 = last[last.Time == 21].groupby("Diet").size()
    drop = last[last.Time < 21][["Time", "weight", "Diet"]]
    return enrolled, at21, drop


def figure1(d, enrolled, at21, out):
    """Q1: per-diet small multiples, shared scales, every chick drawn.

    The full 50-chick cohort is repeated as a light backdrop in every panel so
    the cross-diet overlap asserted in the title is visible without a panel
    jump. Chicks that left early stop at an open circle: a line is never drawn
    across days on which the chick was not weighed.
    """
    all_tr = [g[["Time", "weight"]].values for _, g in d.groupby("Chick")]
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.6), sharex=True, sharey=True)
    for ax, k in zip(axs, [1, 2, 3, 4]):
        for tr in all_tr:
            ax.plot(tr[:, 0], tr[:, 1], color=BACK, lw=0.5, zorder=0,
                    label="all 50 chicks (same in every panel)"
                    if (k == 1 and tr is all_tr[0]) else None)
        g = d[d.Diet == k]
        for cid, gc in g.groupby("Chick"):
            ax.plot(gc.Time, gc.weight, color=OWN, lw=0.8, alpha=0.75, zorder=2,
                    label="chick on this diet"
                    if (k == 1 and cid == g.Chick.iloc[0]) else None)
            if gc.Time.iloc[-1] < 21:
                ax.plot(gc.Time.iloc[-1], gc.weight.iloc[-1], "o", ms=3.6,
                        mfc="white", mec="0.35", mew=0.9, zorder=3,
                        label="left study early" if (k == 1 and cid == 18) else None)
        m = g.groupby("Time")["weight"].mean()
        ax.plot(m.index, m.values, color=PAL[k], lw=2.1, zorder=4,
                label="diet mean" if k == 1 else None)
        ax.set_title("Diet %d\n%d chicks (%d at day 21)" % (k, enrolled[k], at21[k]))
        ax.set_xticks([0, 5, 10, 15, 20])
        ax.margins(x=0.04)

    axs[0].set_ylim(0, 400)
    axs[0].set_ylabel("Body weight (g)")
    axs[0].legend(loc="upper left", fontsize=5.5, handlelength=1.4,
                  borderpad=0.1, labelspacing=0.22)
    axs[0].annotate("mean over chicks measured that day", xy=(0.03, 0.02),
                    xycoords="axes fraction", fontsize=5.5, color="0.35", va="bottom")
    fig.supxlabel("Age (days)")
    fig.suptitle("Diet 1 has the lowest mean weight from day 2 onward, yet individual "
                 "chicks from all four diets overlap between 196 and 305 g at day 21")
    fig.tight_layout()
    issues = audit_figure(fig, verbose=False)
    fig.savefig(out)
    return issues


def figure2(d, drop, out):
    """Q2: the day-21-only comparison, and what restricting to it costs.

    Panel a keeps every measured chick as a point with the enrolled denominator
    under each diet, and plots each absent chick's last weight as an open circle
    so the direction of the survivor bias is visible, not just its count.
    Panel b plots the contrast itself against an explicit zero reference.
    """
    d21 = d[d.Time == 21]
    ci, contr = {}, []
    ref = d21[d21.Diet == 1]["weight"].values
    for k in [1, 2, 3, 4]:
        x = d21[d21.Diet == k]["weight"].values
        h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
        ci[k] = (x.mean(), x.mean() - h, x.mean() + h, len(x))
        if k != 1:
            se = np.sqrt(x.var(ddof=1) / len(x) + ref.var(ddof=1) / len(ref))
            dof = stats.ttest_ind(x, ref, equal_var=False).df
            crit = stats.t.ppf(0.975, dof)
            contr.append((k, x.mean() - ref.mean(),
                          x.mean() - ref.mean() - crit * se,
                          x.mean() - ref.mean() + crit * se))

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.2, 3.0),
                                   gridspec_kw={"width_ratios": [1.3, 1]})
    rng = np.random.default_rng(7)
    for k in [1, 2, 3, 4]:
        x = d21[d21.Diet == k]["weight"].values
        axA.plot(k + rng.uniform(-0.14, 0.14, len(x)), x, "o", ms=3.2, mfc=PAL[k],
                 mec="white", mew=0.4, alpha=0.95, lw=0, zorder=2,
                 label="chick measured at day 21" if k == 1 else None)
        dk = drop[drop.Diet == k]
        if len(dk):
            axA.plot([k - 0.33] * len(dk), dk.weight.values, "o", ms=3.6, mfc="white",
                     mec="0.35", mew=0.9, lw=0, zorder=2,
                     label="absent chick: last weight before leaving" if k == 1 else None)
        m, lo, hi, _ = ci[k]
        axA.plot([k + 0.30] * 2, [lo, hi], color="0.15", lw=1.3, zorder=3,
                 label="mean \u00b1 95% t CI (day-21 chicks)" if k == 1 else None)
        axA.plot(k + 0.30, m, "D", ms=4, color="0.15", zorder=4)

    axA.set_xticks([1, 2, 3, 4])
    axA.set_xticklabels(["Diet %d\n%d of %d" % (k, ci[k][3],
                                                ci[k][3] + (drop.Diet == k).sum())
                         for k in [1, 2, 3, 4]])
    axA.set_ylim(0, 400)
    axA.set_xlim(0.5, 4.6)
    axA.set_ylabel("Body weight at day 21 (g)")
    axA.set_xlabel("Diet (chicks measured at day 21 of chicks enrolled)")
    axA.legend(loc="upper left", fontsize=5.5, handlelength=1.2, borderpad=0.1,
               labelspacing=0.22, numpoints=1)
    locf = np.concatenate([ref, drop[drop.Diet == 1]["weight"].values]).mean()
    axA.annotate("All 5 absent chicks were last weighed below\ntheir diet's day-21 "
                 "mean, so the diet 1 mean\nhere is survivor-inflated (%.1f g with their"
                 "\nlast weights carried forward). Points jittered." % locf,
                 xy=(0.40, 0.33), xycoords="axes fraction", fontsize=5.5,
                 color="0.35", va="top")

    for i, (k, diff, lo, hi) in enumerate(contr):
        axB.plot([lo, hi], [-i, -i], color=PAL[k], lw=1.6, zorder=3)
        axB.plot(diff, -i, "o", ms=5, color=PAL[k], zorder=4)
    axB.axvline(0, color="0.3", lw=0.9, ls=(0, (3, 2)), zorder=1)
    axB.set_yticks([0, -1, -2])
    axB.set_yticklabels(["Diet %d\n(%d vs %d)" % (k, ci[k][3], ci[1][3])
                         for k in [2, 3, 4]])
    axB.set_ylim(-2.55, 0.62)
    axB.set_xlim(-40, 165)
    axB.set_xlabel("Difference in mean day-21 weight\nvs diet 1 (g)")
    axB.annotate("no difference\nvs diet 1", xy=(0, 0.30), fontsize=5.5, color="0.3",
                 ha="center", va="bottom")
    axB.annotate("Welch 95% CI", xy=(0.97, 0.04), xycoords="axes fraction",
                 fontsize=5.5, color="0.35", ha="right")
    panel_letter(axA, "a")
    panel_letter(axB, "b")
    fig.suptitle("Compared only at day 21, diets 3 and 4 exceed diet 1 with intervals "
                 "excluding zero\n\u2014 but the 5 absent chicks were all small, which "
                 "inflates the diet 1 reference")
    fig.tight_layout()
    issues = audit_figure(fig, verbose=False)
    fig.savefig(out)
    return issues, ci, contr


def main():
    style()
    d = load()
    enrolled, at21, drop = cohort(d)
    outdir = os.path.join(HERE, "figures")
    os.makedirs(outdir, exist_ok=True)

    i1 = figure1(d, enrolled, at21, os.path.join(outdir, "fig1_growth_trajectories.png"))
    i2, ci, contr = figure2(d, drop, os.path.join(outdir, "fig2_final_measurement.png"))

    for k in [1, 2, 3, 4]:
        print("diet %d: day-21 mean %.1f g, 95%% CI %.1f to %.1f, n = %d"
              % (k, ci[k][0], ci[k][1], ci[k][2], ci[k][3]))
    for k, diff, lo, hi in contr:
        print("diet %d vs diet 1: %+.1f g, Welch 95%% CI %.1f to %.1f" % (k, diff, lo, hi))
    print("figure 1 violations:", i1)
    print("figure 2 violations:", i2)
    if i1 or i2:
        sys.exit("audit_figure reported unresolved violations")


if __name__ == "__main__":
    main()
