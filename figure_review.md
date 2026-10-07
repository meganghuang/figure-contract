# Figure review — ChickWeight growth figures

Rubric: the `figure-contract` house rules (five promises: Magnitude, Meaning, Evidence, Context, Claim).
Both figures were read as rendered PNGs first; the data (`chickweight.csv`, 578 rows, 50 chicks) was used
only to test the two claim-titles and the printed n's against every row. Findings from the image and
findings from the data are kept separate below.

---

## Figure 1 — growth trajectories by diet (answers Q1)

**Does it answer its question?** First half, yes — unambiguously. Second half, only partly. The four
panels on a shared 0–400 g scale make the trajectory differences legible (diet 1 flattest, diet 3
steepest), and within-diet spread is plain to read: diet 4's chicks run as a tight band, diet 2's fan
apart to the point that one chick flatlines near the bottom of the panel while another is near the top.
But the headline's second clause is a claim about overlap *across all four diets*, and that is the one
comparison the small-multiple layout makes hardest — the diets are in four separate panels, so the reader
must jump and hold positions in memory to check it.

| Promise | Verdict | Evidence seen in the image |
|---|---|---|
| **Magnitude** | keeps | Shared y-axis 0–400 g across all four panels; tick positions and baselines align, so the tallest diet-3 trajectory (~375 g) reads as genuinely above the tallest diet-1 trajectory (~305 g). Lines are position encodings, no truncated length or area encoding, no 3D, no twin axis. |
| **Meaning** | keeps | Lines join repeated measures on the same chick in time order — the one ordering that licenses a line. Legend in panel 1 defines all three marks: thin gray = individual chick, open circle = left study early, thick colored = diet mean. Dropout trajectories stop at a circle rather than being carried to day 21. The in-panel note "mean is over chicks measured on each day" states that the mean's denominator shrinks over time. |
| **Evidence** | keeps | n is on every panel in both forms that matter: enrolled and still present at day 21 ("20 chicks (16 at day 21)"). The experimental unit is the chick and every chick is drawn individually; pairing is preserved as a trajectory rather than collapsed to a mean. There are no error bars, so there is no interval definition to miss — showing all observations is the stronger form here. |
| **Context** | keeps | Denominators per panel, attrition marked at the point and weight where each chick left, the shifting composition of the mean stated in words, raw grams with no transform, and the full measured range (day 0–21) shown. |
| **Claim** | keeps | "Diet 1 has the lowest mean weight from day 10 onward, but individual chicks overlap across all four diets." Verified against every row (below). The title is conservative rather than overreaching, and carries no causal language. |

**Claim verification against the data.** Diet 1 has the lowest mean at *every* measured day from 10 to 21
(93.1, 108.5, 123.4, 144.6, 158.9, 170.4, 177.8 g) — and in fact from day 2 onward; only at day 0 is any
other diet lower (diet 2 at 40.7 vs 41.4 g). All six pairwise day-21 ranges overlap, and the band
196–305 g contains chicks from all four diets, so the overlap clause is true of every row. Panel n's are
exact (20/16, 10/10, 10/10, 10/9), and all five dropout circles match real last observations.

**Most damaging problem.** The title asserts a cross-diet comparison that the layout suppresses. Four
separate panels are the right choice for showing *within*-diet consistency, but they make "individual
chicks overlap across all four diets" an act of faith — nothing in the figure puts a diet-1 chick next to
a diet-3 chick on a common vertical line. A reader who takes the first clause at face value and skims the
second will leave with "diet 1 is worse" and no feel for how completely the distributions interleave.

**Fixes (the change to make).**
1. Draw all 50 trajectories as a very light gray silhouette behind each panel's own chicks, so every panel
   carries the whole cohort as its backdrop and the overlap is visible without a panel jump.
2. Alternatively or additionally, add a fifth narrow panel at the right: day-21 weight as one strip of
   points per diet on the same 0–400 g y-axis — the overlap then reads on a single shared axis.
3. Set the individual chick lines to ~40–50% alpha. In the diet-1 panel, 20 solid gray lines merge into one
   mass between roughly 100 and 250 g at day 16–21; the envelope is readable but individual trajectories in
   the interior are not.
4. State the mean's definition more completely in the annotation: "mean of chicks measured that day
   (n falls from 20 to 16 on diet 1)" — the present wording says the denominator changes but not by how much.

**What a reader cannot verify without the data.**
- Whether any chick has an interior unmeasured day that a line crosses. (It does not — no chick in the
  dataset is missing a day between its first and last measurement — so the figure is clean here, but the
  figure cannot tell you that.)
- Whether every enrolled chick is actually drawn. The lines merge; they cannot be counted against the
  panel's stated n.
- Whether "diet mean" is an unweighted mean over chicks present that day, as the annotation says.
- That "from day 10 onward" is not the earliest day the claim holds — it holds from day 2.

---

## Figure 2 — day-21 comparison (answers Q2)

**Does it answer its question?** Yes. The title names the restriction ("Compared only at day 21"), panel a
shows what survives it with every chick as a point, and panel b shows the consequence: only diets 3 and 4
separate from diet 1 with intervals excluding zero, while diet 2's interval straddles it. What changes is
stated as a loss of both data and certainty, which is exactly the answer Q2 wants. The one thing it cannot
convey on its own is the magnitude of what was discarded — 11 earlier timepoints — which only Figure 1
supplies.

| Promise | Verdict | Evidence seen in the image |
|---|---|---|
| **Magnitude** | keeps | No length-from-baseline encoding anywhere: points and intervals in panel a, dots with intervals in panel b. Panel a's y-axis runs 0–400 g, matching Figure 1, so weights are comparable across the pair. Panel b is a linear difference axis with an explicit dashed zero reference — the correct treatment for a contrast. |
| **Meaning** | keeps | Legend in panel a names both marks and the interval ("individual chick"; "mean ± 95% t CI"). Panel b's x-axis title states the contrast explicitly ("Difference in mean day-21 weight vs diet 1"), and the interval type is labeled in-panel ("Welch 95% CI"). Nothing is joined by a line. Two defects that cost the reader, short of a broken promise: the zero line is annotated "no change", which describes a within-subject change rather than a between-diet difference, and panel b's rows run Diet 4 → 3 → 2 top-to-bottom against panel a's Diet 1 → 4 left-to-right, so the eye has to invert the order to move between panels. |
| **Evidence** | keeps | Every day-21 chick is plotted, not just a summary. n is under each diet as a fraction of the enrolled group ("16 of 20"), which gives the reader the numerator and denominator at once. Each interval is defined by name in the panel where it appears. The unit is the chick with one measurement each, so n and the independent unit coincide here and the figure says so. |
| **Context** | keeps | Exclusions are counted and attributed in-panel: "5 chicks absent: they left the study before day 21 (4 on diet 1, 1 on diet 4)", repeated in the title as "5 of 50". The per-diet denominators are on the x-axis, no transform, and the restriction to a single day is in the title rather than left implicit. |
| **Claim** | keeps | "Compared only at day 21, diets 3 and 4 exceed diet 1 with intervals excluding zero — but 5 of 50 chicks are absent." Every element checks out against the data (below), and the title claims interval exclusion rather than an effect, which is what the design supports. |

**Claim verification against the data.** Welch 95% CIs for the difference in mean day-21 weight vs diet 1:
diet 3 (+35.5, +149.6), diet 4 (+18.0, +103.6) — both exclude zero; diet 2 (−24.2, +98.1) includes it, and
the figure draws it crossing the line. Counts are exact: 50 enrolled, 45 measured at day 21, the 5 absent
split 4 on diet 1 and 1 on diet 4.

**Most damaging problem.** Panel b's reference group is the one diet that lost 4 of its 20 chicks, and the
five chicks that left were small — their last weights were 35, 54, 68, 125 and 146 g, every one below the
day-21 *mean* of its own diet (diet 1 mean 177.8 g, diet 4 mean 238.6 g), and four of the five below their
diet's day-21 *minimum*; the exception is chick 8, last weighed at 125 g on day 20, above diet 1's day-21
minimum of 96 g but still 53 g below the diet-1 mean. Diet 1's day-21 mean is therefore inflated by
survivorship (177.8 g among survivors; 156.3 g if each dropout's last observation is carried forward), so
the disclosed caveat points the wrong way: a reader handed "but 5 of 50 chicks are absent" will read it as
a reason to discount the diet 3/4 advantage, when the attrition is in fact shrinking that advantage. The
figure discloses the *count* honestly and gives the reader no way to sign the bias.

**Fixes (the change to make).**
1. In panel a, plot each absent chick's last observed weight as an open circle at its diet — same open-circle
   convention as Figure 1 — and label them "last weight before leaving, not day 21". The reader then sees
   immediately that the missing chicks sit below the measured ones.
2. Change the annotation from a bare count to a direction: "5 chicks absent (4 on diet 1, 1 on diet 4);
   all were last weighed below their diet's day-21 mean, so diet 1's mean here is survivor-inflated."
3. Reorder panel b to Diet 2 → 3 → 4 top-to-bottom so it matches panel a's left-to-right order.
4. Relabel the zero line "no difference vs diet 1" instead of "no change".
5. Extend panel b's x-limit to about −40 g. Diet 2's lower bound (−24.2 g) currently ends at the extreme
   left edge of the panel, where a reader cannot tell the end of an interval from a clipped one.
6. Put n on panel b's rows (e.g. "Diet 4 (9 vs 16)") so the panel stands on its own, and state the jitter
   ("points jittered horizontally") in panel a.

**What a reader cannot verify without the data.**
- Whether the 5 absent chicks were large or small — i.e. the direction of the survivor bias on the diet-1
  reference. (Data: all five last weighed below their diet's day-21 mean, as above. Figure 1 shows this;
  Figure 2 does not.)
- Whether two near-coincident points in panel a are two chicks or one mark, since the jitter is undisclosed.
- The Welch degrees of freedom behind each interval, and the exact interval limits — the dots and whiskers
  are readable to perhaps ±5 g.
- Whether the three intervals against a common reference carry any multiplicity adjustment. None is stated,
  and none is applied; the diet 3 and diet 4 contrasts would survive a Bonferroni threshold anyway
  (p = 0.0033 and p = 0.0076 against α = 0.0167), but the figure gives the reader no way to know that.
- Whether panel a's CI is the t interval it claims rather than a normal approximation.

---

## Summary

Both figures keep all five promises. That is not a courtesy verdict — the things that usually break here are
all handled: zero-based and shared scales, every observation drawn, n given as measured-of-enrolled, every
interval named, exclusions counted in-panel, and claim-titles that survive a row-by-row check.

The remaining work on each is a reading problem rather than a fidelity problem, and they differ in kind.
Figure 1 asserts a cross-diet overlap its own panel structure prevents the reader from seeing; give every
panel the full cohort as a silhouette and the title becomes self-evidencing. Figure 2 hands the reader a
caveat whose direction only the data reveals, and the fix is small — plot the five absent chicks at their
last weight and say which way the bias runs.
