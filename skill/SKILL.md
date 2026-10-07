---
name: figure-contract
description: "House rules for scientific figures, built on one idea: a figure is a contract between its maker and its reader. Load BEFORE building any figure, plot, or data visualization someone else will read, and when critiquing or revising one. Covers chart choice from the question, proportional encoding and zero baselines, log and fold-change scales, what a line is allowed to mean, missing vs measured, color matched to variable structure, n / experimental unit / pairing / uncertainty, denominators and transforms, titles that the design supports, and panel layout. Ships audit_figure(fig) to check a matplotlib figure against the mechanically checkable rules."
---

# A figure is a contract

*"When I draw it this way, you can reasonably read it this way."*

The reader cannot inspect every analysis decision while looking at a figure, so
the maker owes them inferences that are warranted. **Good design makes the
intended reading easy and the misleading reading difficult.**

Five promises. Every rule below serves one of them; the self-review at the end
is just these five as questions.

| Promise | What it means |
|---|---|
| **Magnitude** | Twice the bar length really means twice the value. |
| **Meaning** | Every line, color, position and distance has a stated interpretation. |
| **Evidence** | The reader can identify n, the experimental unit, pairing and uncertainty. |
| **Context** | Denominators, exclusions and transformations are visible. |
| **Claim** | The title says only what the data and the design support. |

## Workflow

1. **Inspect** — units, ranges, missingness, sample composition, and what the
   independent experimental unit is. Do this before choosing a chart.
2. **Explore broadly** — plain, unstyled plots; distributions, relationships,
   subgroups. Dense views are fine here.
3. **State one question in a sentence**, and name the comparison it needs.
   Exploration and explanation are different jobs; a pairplot that is right for
   the analyst is wrong on a projector.
4. **Pick the chart from the question** (table below), not from habit.
5. **Draw, then audit** — run `audit_figure(fig)` and the five promises.
6. **Refine** — labels, common scales, uncertainty, context. Layout improvement
   must preserve the evidence: never delete observations, controls or
   uncertainty to tidy a figure.

## 1. The question determines the chart

Variable type constrains the options; the comparison decides which option helps.

| Question | Starting point | Key check |
|---|---|---|
| How many? What fraction? | count bars; proportion bars; mosaic | denominator and sample composition |
| How does it vary? | points; histogram; box; violin; ECDF | raw n, bin width or smoothing |
| How do variables relate? | scatter; binned counts; correlation matrix | subgroups, outliers, units |
| How does it change? | time series; paired lines; change plot | order, pairing, missing intervals |
| What pattern spans many features? | heatmap; small multiples | transform, color scale, shared axes |

Chart family is a starting point, not a rule — and the same dataset often needs
several displays during exploration.

**Always, without exception:** every axis labeled with the measurement *and its
units*; a title; every panel and series identified. For bar charts, decide
explicitly whether the question is about **counts**, **proportions within
group**, or **joint composition** — they are three different charts. A
proportion bar hides unequal group sizes; a mosaic keeps them in the width.

## 2. Magnitude — visual size represents numerical value

Principle of proportional ink: when a shaded region represents a value, its
**area** must be proportional to that value.

- **Bars and areas start at zero.** A baseline at 48% turns 49% vs 51% into an
  apparent threefold difference. Truncating a *length* encoding is never
  allowed. If a small difference is the point, use a point-and-interval plot
  with labeled limits.
- **Position encodings (points, lines) may use a focused range.** They encode
  position from an axis, not length from a baseline, so zero is not required —
  but keep every observation and disclose the limits. Never let an automatic
  range quietly hide relevant context.
- **No 3D, perspective or depth** for quantitative comparison. The comparison
  must survive the camera angle: side walls, receding baselines and occluded
  marks create work unrelated to the question. This is about comparison tasks,
  not a blanket ban on pie charts — but two slices of similar size are not
  comparable by eye, and a common-baseline bar is.
- **Area and radius encode different quantities.** For bubbles, area ∝ value
  (so r ∝ √value); radius ∝ value makes a 3× difference look like 9×. For
  precise comparison, aligned dots or bars beat bubbles.
- **Comparisons need a common axis.** Same height on the same scale means the
  same value. Separate panels for different outcomes or units.
- Dependent variable on **y**, typically.

## 3. Scales and transforms

- **Linear and logarithmic views answer different questions** — absolute
  differences vs constant ratios. Both are legitimate; the transform belongs in
  the axis label (`log₂ expression`, not `expression`).
- A logarithm **cannot represent zero or negative values**. Never silently drop
  them. A pseudocount changes low-value ratios; a nonlinear transform can change
  a Pearson correlation. Say what you did.
- **Fold change has a natural reference**: ratio = 1, log₂FC = 0. Draw that
  reference line. Use dots, not bars — a bar has no finite zero on a log scale.
  Log₂ puts 2× and 0.5× at equal distances from the center.
- **Equal visual distance must have an explicit quantitative meaning.** Ticks at
  90, 99, 99.9, 99.99 are not equal increments; an expanded tail changes every
  slope and shape judgment. Label it, or split body and tail into described
  panels. Likewise a *bin index* axis is not a value axis — equal index spacing
  must not be read as equal intervals.
- **Unequal-width bins:** plot frequency *density* so area is proportional to
  frequency.
- **Comparing distributions requires common bins and a common range** (same
  edges, same count axis) — otherwise per-panel defaults change the comparison.
- **Bin width is a choice, not a fact.** Check that the conclusion survives
  reasonable widths: coarse bins merge two clusters, very narrow bins exaggerate
  noise. This is a sensitivity check, not permission to pick the most dramatic
  version.

## 4. Meaning — what a line, gap or distance promises

- **A line means a connection.** Meaningful order justifies it: time, spatial
  path, within-subject pairs. Arbitrary order does not — joining independent
  observations in file order invents a trajectory. Use a scatterplot.
- **Plot fits separately from observations** and label them as fits.
- **Missing is not measured, and not zero.** Deleting missing rows and joining
  what remains draws a line across hours that were never sampled. Leave the gap
  and state it ("hours 3–5 not measured"). Observed, estimated and interpolated
  values get visually distinct treatment; if you show interpolation, say what
  model produced it.

## 5. Visibility — you must be able to follow every population

- **A hidden mark is not an absent observation.** Occluded bars or lines cannot
  be read as low values.
- **A series needs space to remain visible.** Past roughly 5–6 overlapping
  series, or whenever lines cross repeatedly, switch to small multiples with
  **shared x and y limits** and direct panel labels. Shared scales preserve
  magnitude comparison while removing legend lookup. Per-panel scales can serve
  within-series *shape* comparison, but then say so and accept that cross-panel
  magnitude comparison is gone.
- **Never use independent dual y-axes.** Their arbitrary ranges manufacture
  visual alignment.
- **Overplotting hides coincident observations.** Options: transparency, smaller
  marks, jitter for discrete values, 2-D binned counts, hexbins, density. State
  the bin size or bandwidth; a smoothed density's colors are not counts unless
  you define them that way.
- **Prefer direct labels to legend lookup.**

## 6. Color matches the structure of the variable

| Variable | Scale | Notes |
|---|---|---|
| Unordered groups | multiple distinct **hues** | categorical |
| Increasing magnitude | one hue, ordered **lightness** | sequential |
| Change around a center | two hues, negative / positive, ordered values each side | diverging |

- **Define the scale** — quantity, units, limits, the center, and any transform.
  A colorbar without a defined meaning is a broken promise.
- A diverging scale's center must be the **meaningful** value (no change, 0),
  never the midpoint of the observed range.
- **No rainbow / jet.** Uneven hue and lightness steps invent rings and
  boundaries in a perfectly smooth field. Grayscale is a useful ordering check
  but is not a substitute for color-vision-deficiency testing.
- **Color alone is a fragile label.** Red/green plus a legend fails for many
  readers and collapses in grayscale. Add named panels, marker shapes, line
  patterns or direct labels. Test at final size, in grayscale, and with a CVD
  simulation. A palette name alone does not guarantee access.
- **Same group → same color in every panel and every figure of the set.**

## 7. Evidence — n, the unit, pairing, uncertainty

- **Identical means do not imply similar observations.** Means alone hide
  bimodality, gaps, skew and outliers. Show every observation when n is small;
  with large n use a distribution display that still exposes shape.
- **The experimental unit determines the independent n.** 36 cells from 3
  treated cultures is n = 3, not 36. Show the unit structure (small points for
  cells, large points for culture means) and analyze at the unit level or with a
  hierarchical model. More cells measure a culture better; they do not create
  independent replicates.
- **An error bar has a definition — label it, with its n.** From one dataset
  (n = 25, mean 10, SD 4): SD = 4 (spread of observations), SE = 0.8
  (uncertainty of the mean), 95% CI ≈ 10 ± 1.65 (interval for the mean). Same
  data, three different meanings.
- Overlap of two separate intervals is **not** a significance test. If the
  contrast matters, plot the contrast and its interval.
- **Paired data keeps its pairing** — in the display and in the analysis. Show
  per-subject trajectories, and the within-subject differences against a zero
  reference.
- **Box and violin caveats.** A box is Q1–Q3 with the median; it can hide
  multiple modes, and whisker/outlier conventions vary by library — state
  yours. A violin's width is smoothing, not sample size, and the density can
  extend past the measurement bounds (scores beyond 0–100) — constrain it. For
  small samples, show the points. Neither reveals the number of independent
  units.
- **State exclusions**: how many rows, why, and exclude on the variables
  actually used rather than dropping rows with unrelated missing fields.

## 8. Context — what the reader needs to interpret the comparison

- **A percentage needs a denominator.** Put group n in the label or encode it
  (mosaic width).
- **Pooling can reverse a comparison.** A treatment can win within every
  severity stratum and lose on the pooled rate because the case mix differs
  (Simpson's paradox). Check stratification before plotting a pooled rate;
  stratifying is a diagnostic, not automatic causal adjustment.
- **Report the transform.** Row z-scoring a heatmap removes magnitude and
  spread: after scaling, identical colors can be measurements that differ
  tenfold, and a constant row is undefined. Say whether color is raw level or a
  within-feature z-score, and disclose any clustering.
- A **correlation matrix** summarizes associations in this sample and omits
  shape, outliers and subgroup structure. It should send the reader back to
  scatterplots, not replace them. Pooling subgroups changes the coefficients.
- A visible pattern of missingness does not identify its mechanism.

## 9. Claim — the title

- The title says **only what the data and design support**. No causal language
  without a design that establishes causation.
- Prefer a specific takeaway over a generic label — name the outcome, the units
  and the intended comparison ("Drug B is 6 U/mL above control") rather than
  "Response by group". But a claim-title must be true of **every** row in the
  plot, and it never licenses dropping the other groups: keep the full context
  and let the title point at the planned contrast.
- A figure can be technically faithful and still incomplete. Before calling it
  done, check it carries n, distributions and a defined interval.

## 10. Complexity and audience

- **Complexity is a tradeoff between the information available and the
  information a viewer can read.** Dense is not automatically bad — it is bad
  for the wrong venue.
- Exploration: inspect and compare, as dense as you like. A talk: one
  comparison at a time; introduce encodings separately, or show a focused crop
  with context. Print or interactive: patient inspection is possible.
- **Panel alignment supports scientific reading.** Keep order, labels and scales
  consistent across panels; match image column order to the order of the
  quantitative comparison beside it. Ask which comparisons force the reader's
  eye to jump between panels — and remove that jump.
- Layout improvement must preserve the evidence.

## Self-review before saving

Run `audit_figure(fig)` for the mechanical checks, then answer these by hand:

1. **Magnitude** — is every length/area encoding proportional, from zero, free
   of perspective?
2. **Meaning** — does every line, gap, color and equal distance have a stated
   interpretation?
3. **Evidence** — can a reader find n, the experimental unit, the pairing, and
   the definition of every interval?
4. **Context** — are denominators, exclusions and transforms visible on the
   figure?
5. **Claim** — would the title survive a reviewer who only had this figure?

Then: does the figure still work in grayscale, and at the size it will be shown?

## Tooling

**Python** — `audit_figure(fig)`, `contract_checklist()`, `diverging_norm()`,
`apply_shared_limits()`, `symmetric_limits()`, `label_n()` are loaded with this
skill (see `kernel.py`). Call `audit_figure(fig)` before `fig.savefig(...)`.
For typographic polish (font ladder, ticks, dpi) load **figure-style**; for
multi-panel composition load **figure-composer**; for a whole paper's figure arc
load **paper-narrative**. Those govern *look*; this skill governs *correctness*
and wins any conflict.

**R / ggplot2** — the same rules map directly:

- zero baseline: `expand_limits(y = 0)` with `geom_col`; never `coord_cartesian(ylim = c(48, 52))` on bars
- shared scales: `facet_wrap(..., scales = "fixed")` (the default — don't set `"free"` without saying why)
- diverging color with a real center: `scale_fill_gradient2(midpoint = 0)`
- sequential: `scale_fill_viridis_c()`; never `rainbow()` / `scale_*_gradientn(colours = rainbow(n))`
- missing gaps: keep `NA` rows instead of `drop_na()` — `geom_line` breaks at `NA`
- show the points: `geom_quasirandom()` / `geom_jitter(width = 0.15)` over `geom_col` of means
- nested units: `geom_point(alpha = .3)` for cells + `stat_summary` per culture
- labels: `labs(x = , y = , title = , caption = )` on every plot; units in the axis title
- Seurat: `DimPlot`/`FeaturePlot` defaults break several rules — set `cols=` for consistent group colors across every panel, use `max.cutoff`/`min.cutoff` deliberately and state the cutoff, and remember a row-scaled `DoHeatmap` is a z-score, not expression.

## Provenance

Codified from the user's *Lecture 2 — Data visualization* deck (the
figure-as-contract framework, its published critique examples and speaker
notes) plus their own stated rules. Supporting sources named in the deck:
Weissgerber et al. 2015 (PLoS Biol); Cumming et al. 2007 (JCB); Lord et al. 2020
(JCB, experimental unit); Crameri et al. 2020 (Nat Commun, color); Matejka &
Fitzmaurice 2017 (same stats, different graphs). The notes to slides 3 and 21
additionally link a reading as `cleveland84.pdf` without naming it; that file is
Cleveland & McGill's 1984 graphical-perception paper, identified here from the
URL rather than cited by the deck, and it underlies the position-over-length and
common-axis rules.
