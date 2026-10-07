import os

RAINBOW_CMAPS = ("jet", "rainbow", "gist_rainbow", "hsv", "nipy_spectral", "turbo", "gist_ncar", "flag", "prism")

CONTRACT = (
    "Magnitude: twice the bar length really means twice the value.",
    "Meaning: every line, color, position and distance has a stated interpretation.",
    "Evidence: the reader can identify n, the experimental unit, pairing and uncertainty.",
    "Context: denominators, exclusions and transformations are visible.",
    "Claim: the title says only what the data and the design support.",
)


def contract_checklist():
    """Print the five promises of the figure contract."""
    for i, line in enumerate(CONTRACT, 1):
        print(str(i) + ". " + line)


def title_text(ax):
    """Panel title text regardless of its loc.

    set_title() writes to the location named by rcParams['axes.titlelocation'],
    so get_title() -- which defaults to loc='center' -- returns '' for every
    left-aligned title, i.e. for the house style. Check all three locations.
    """
    for loc in ("center", "left", "right"):
        try:
            t = (ax.get_title(loc=loc) or "").strip()
        except Exception:
            t = ""
        if t:
            return t
    return ""


def panel_name(ax):
    """Short human label for an Axes."""
    t = title_text(ax)
    if t:
        return t[:40]
    try:
        ss = ax.get_subplotspec()
        return "row %d col %d" % (ss.rowspan.start, ss.colspan.start)
    except Exception:
        return "axes"


def numeric_tick_labels(ax, which="x"):
    """True when every visible tick label on that axis parses as a number.

    A categorical axis whose ticks name the categories ("Diet 1", "Gentoo") is
    self-labeling: an axis title restating the tick labels is an anti-pattern.
    """
    ticks = ax.get_xticklabels() if which == "x" else ax.get_yticklabels()
    texts = [t.get_text().strip() for t in ticks if t.get_text().strip()]
    if not texts:
        return True
    for t in texts:
        clean = t.replace("\u2212", "-").replace(",", "").replace("%", "")
        clean = clean.split("\n")[0].strip()
        try:
            float(clean)
        except ValueError:
            return False
    return True


def audit_figure(fig, max_series=6, verbose=True):
    """Check a matplotlib Figure against the mechanically checkable contract rules.

    Returns a list of {panel, rule, detail}. Silence is not a passing grade:
    n, the experimental unit, denominators, exclusions and the claim in the
    title still need the by-hand checklist in SKILL.md.
    """
    from matplotlib.patches import Rectangle
    from matplotlib.colors import to_hex
    issues = []
    # a colorbar is not a panel: it carries no x/y measurement of its own
    axes = [a for a in fig.get_axes()
            if a.get_visible() and getattr(a, "_colorbar", None) is None]

    def flag(ax, rule, detail):
        issues.append({"panel": panel_name(ax) if ax is not None else "figure",
                       "rule": rule, "detail": detail})

    suptitle = ""
    try:
        suptitle = (fig.get_suptitle() or "").strip()
    except Exception:
        suptitle = "".join(t.get_text() for t in fig.texts).strip()
    if not suptitle and not any(title_text(a) for a in axes):
        flag(None, "no title", "figure has neither a suptitle nor any panel title")

    suplabels = {"x": "", "y": ""}
    for which, getter in (("x", "get_supxlabel"), ("y", "get_supylabel")):
        try:
            suplabels[which] = getattr(fig, getter)() or ""
        except Exception:
            attr = getattr(fig, "_sup" + which + "label", None)
            suplabels[which] = attr.get_text() if attr is not None else ""

    seen_bbox = {}
    for ax in axes:
        has_data = bool(ax.lines or ax.collections or ax.patches or ax.images or ax.containers)
        if not has_data:
            continue

        for which in ("x", "y"):
            own = (ax.get_xlabel() if which == "x" else ax.get_ylabel()) or ""
            if own.strip():
                continue
            if suplabels.get(which, "").strip():
                continue
            try:
                grp = ax.get_shared_x_axes() if which == "x" else ax.get_shared_y_axes()
                sibs = list(grp.get_siblings(ax))
            except Exception:
                sibs = [ax]
            labeled = any(((s.get_xlabel() if which == "x" else s.get_ylabel()) or "").strip()
                          for s in sibs if s is not ax)
            if not numeric_tick_labels(ax, which):
                continue
            if not labeled:
                flag(ax, "unlabeled axis",
                     which + "-axis has no label on this panel, on a shared sibling, or on the figure "
                     "(measurement + units required)")

        for which, scale, label in (("x", ax.get_xscale(), ax.get_xlabel()),
                                    ("y", ax.get_yscale(), ax.get_ylabel())):
            if scale != "linear" and "log" not in (label or "").lower():
                flag(ax, "undisclosed transform",
                     which + "-axis scale is '" + scale + "' but the label does not say so")

        bars = [p for p in ax.patches if isinstance(p, Rectangle)]
        vertical = [p for p in bars if p.get_width() < p.get_height() or p.get_y() == 0]
        if ax.containers or len(bars) > 1:
            lo, hi = ax.get_ylim()
            if bars and min(lo, hi) > 0 and len(vertical) >= len(bars) / 2.0:
                flag(ax, "truncated length encoding",
                     "bars present but y-axis starts at %.4g, not 0" % min(lo, hi))
            bottoms = [p.get_y() for p in vertical]
            if bottoms and min(bottoms) != 0 and max(bottoms) == min(bottoms):
                flag(ax, "non-zero bar baseline", "bar bottoms sit at %.4g" % min(bottoms))

        styles = set()
        for ln in ax.lines:
            if ln.get_linestyle() in ("None", "none") or (ln.get_linewidth() or 0) <= 0:
                continue
            try:
                styles.add((to_hex(ln.get_color()), str(ln.get_linestyle())))
            except Exception:
                styles.add((str(ln.get_color()), str(ln.get_linestyle())))
        if len(styles) > max_series:
            flag(ax, "too many distinguishable series",
                 "%d distinct line colors/styles in one panel (> %d): legend lookup burden, "
                 "use small multiples with shared limits. (An ensemble drawn in one de-emphasized "
                 "color counts once and is not flagged.)" % (len(styles), max_series))

        for art in list(ax.images) + list(ax.collections):
            cmap = getattr(art, "get_cmap", None)
            name = cmap().name if cmap is not None and cmap() is not None else ""
            if name in RAINBOW_CMAPS:
                flag(ax, "rainbow colormap", "'" + name + "' has uneven lightness; use sequential or diverging")
        for im in ax.images:
            if getattr(im, "colorbar", None) is None:
                flag(ax, "undefined color scale", "image drawn without a colorbar")

        key = tuple(round(v, 4) for v in ax.get_position().bounds)
        if key in seen_bbox:
            flag(ax, "dual axis", "shares a position with '" + seen_bbox[key] + "'; independent twin axes are not allowed")
        seen_bbox[key] = panel_name(ax)

    groups = {}
    for ax in axes:
        lab = (ax.get_ylabel() or "").strip()
        if lab:
            groups.setdefault(lab, []).append(ax)
    for lab, group in groups.items():
        lims = set(tuple(round(v, 6) for v in a.get_ylim()) for a in group)
        if len(group) > 1 and len(lims) > 1:
            flag(group[0], "panels not on a common scale",
                 "%d panels labeled '%s' have %d different y-limits" % (len(group), lab, len(lims)))

    if verbose:
        if not issues:
            print("audit_figure: no mechanical violations. Now run the by-hand checks:")
            contract_checklist()
        else:
            for it in issues:
                print("[" + it["rule"] + "] " + it["panel"] + ": " + it["detail"])
    return issues


def symmetric_limits(values):
    """(-m, m) with m = max |value| — for a diverging scale centered on 0."""
    import numpy as np
    m = float(np.nanmax(np.abs(np.asarray(values, dtype=float))))
    return (-m, m)


def diverging_norm(values, center=0.0):
    """TwoSlopeNorm anchored on a MEANINGFUL center (0 for log fold change)."""
    import numpy as np
    from matplotlib.colors import TwoSlopeNorm
    arr = np.asarray(values, dtype=float)
    lo, hi = float(np.nanmin(arr)), float(np.nanmax(arr))
    pad = 1e-9 * (abs(hi) + abs(lo) + 1.0)
    return TwoSlopeNorm(vmin=min(lo, center - pad), vcenter=center, vmax=max(hi, center + pad))


def apply_shared_limits(axes, axis="both"):
    """Force a common scale across panels so heights are comparable."""
    axes = list(axes)
    if axis in ("x", "both"):
        lo = min(a.get_xlim()[0] for a in axes)
        hi = max(a.get_xlim()[1] for a in axes)
        for a in axes:
            a.set_xlim(lo, hi)
    if axis in ("y", "both"):
        lo = min(a.get_ylim()[0] for a in axes)
        hi = max(a.get_ylim()[1] for a in axes)
        for a in axes:
            a.set_ylim(lo, hi)
    return axes


def label_n(ax, counts, axis="x"):
    """Append 'n = k' to category tick labels. counts: dict label -> n, or a list."""
    getter = ax.get_xticklabels if axis == "x" else ax.get_yticklabels
    setter = ax.set_xticklabels if axis == "x" else ax.set_yticklabels
    labels = [t.get_text() for t in getter()]
    if isinstance(counts, dict):
        new = [l + ("\nn = " + str(counts[l]) if l in counts else "") for l in labels]
    else:
        new = [l + "\nn = " + str(n) for l, n in zip(labels, list(counts))]
    setter(new)
    return ax
