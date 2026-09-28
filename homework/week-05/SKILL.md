---
name: stat432-plot-format
description: Improve the formatting of an existing STAT 432 homework plot made in R or Python. Use only when I explicitly ask to use this skill or to format a STAT 432 homework plot; never apply it on your own, and do not use it for other courses, for new analyses, or for changing what a plot computes.
---

# STAT 432 Homework Plot Formatting

Improve how a homework plot looks without changing the data, the model, or the
conclusion it supports. Edit only the plotting code, then re-render and show
the before and after images.

## Rules

- **Size and margins.** Use a figure about 6.5 in wide and 4 in tall (fits a
  letter page with 1 in margins). Save at 200–300 dpi with tight bounding boxes
  (`bbox_inches="tight"` in matplotlib, `ggsave(width = 6.5, height = 4)` in R)
  so nothing is clipped and there is no large empty border.
- **Title.** Give a short, informative title that states what is plotted, in
  sentence case, without "vs." filler or a trailing period. Put setup details
  (sample size, number of replications, fixed point) in a smaller subtitle or
  caption rather than the main title. Keep the title block tight: the
  subtitle sits just above the plot area (a few points of space), the title
  sits directly above the subtitle, and there is no more than about half a
  line of blank space anywhere between the title and the plot. The title and
  subtitle must still never overlap each other or the plot area.
- **Axes.** Label every axis with the quantity in words plus its symbol, e.g.
  "Number of neighbors, k". Show units when they exist. Use integer ticks for
  integer quantities, start a quantity's axis at zero only when zero is
  meaningful, and switch to a log scale only when values span more than one
  order of magnitude.
- **Labels and legends.** Replace code names (`mse`, `bias^2`, column names
  with underscores) with readable math or words, e.g. "Bias²", "Variance",
  "MSE". Place the legend where it covers no data, or label lines directly at
  their ends. Mark a key value (such as a minimum or the selected tuning
  parameter) with a small annotation when the question depends on it. Put the
  annotation text in an empty region of the plot, well clear of every line,
  marker, and the legend (roughly 10% of the axis range or more when space
  allows), and connect it to its point with a thin arrow that stops a few
  points short of the marker.
- **Colors.** Use a colorblind-safe palette (Okabe–Ito or viridis) with at most
  about six distinct colors. Keep the same quantity the same color across plots
  in one submission. Pair color with a second cue (marker shape or line style)
  so the plot still reads in grayscale.
- **Text and marks.** All text at least 9 pt at final size; lines about 1.5–2
  pt; markers small enough not to hide the line. Use a light, low-contrast grid
  or none, and remove top and right spines/borders.
- **Code.** Keep formatting in the plotting call itself (no global style files)
  so the figure reproduces from the submission alone.

## Workflow

1. Render the current plot and note which rules it breaks.
2. Apply only the rules that fix a real problem; do not redesign the chart type.
3. Re-render and look at the saved image itself, not just the code: check for
   overlapping or clipped text, a legend or annotation covering data, and
   anything unreadable at final size. Fix and re-render until it is clean.
4. Save the revised figure under a new name so the original remains for
   comparison, and list the changes in a few bullets.