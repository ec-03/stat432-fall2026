---
name: clustering-report
description: Compare several clustering algorithms on a supplied dataset, select one by pre-set internal criteria, and write a one-page report. Use ONLY when I explicitly invoke this skill by name and supply the data details; never load it on your own.
disable-model-invocation: true
---

# Clustering analysis with a one-page report

The user supplies: the data file, what one observation is, the feature
columns, any ID column, any known label columns, and a seed (pick and state
one if none is given). Keep all code in one reproducible script.

**Labels rule:** never use known labels for preprocessing, tuning, choosing
K, or choosing the method; use them only to interpret the final clustering.

## 1. Preprocess (decide from the features alone, state every choice)

- Check n, p, missing values, constant features, gross outliers.
- Center features. Standardize them only if they have different units or
  scales; if they share a unit, keep the variances.
- If p is much larger than n, also build a reduced version: keep the most
  variable features (unsupervised filter) and/or the leading principal
  components (enough for ~70-90% of variance, or the scree elbow).
- Fix ONE evaluation space and distance used to score every candidate, so
  that scores are comparable.

## 2. Candidates (at least three clustering algorithms)

1. **K-means** (at least 50 random starts).
2. **Hierarchical agglomerative**: Ward, average, and complete linkage;
   Euclidean and, when shape matters more than size, correlation distance.
3. **Spectral clustering**: nearest-neighbor affinity over a small grid of
   neighbor counts (or RBF over a grid of bandwidths).

Run each for K = 2 to about 8 (fewer if n is small). PCA, UMAP, or t-SNE may
preprocess or plot, but never count as a clustering algorithm.

## 3. Criteria and selection rule (fixed before looking at results)

For every algorithm x setting x K record:

- **Average silhouette width** in the evaluation space.
- **Stability**: refit on at least 100 random 80% subsamples; mean adjusted
  Rand index (ARI) against the full-data clustering on shared observations.
- **Smallest cluster size**.

Rule:

1. Drop any candidate with a cluster smaller than max(2, 5% of n).
2. Within each algorithm keep the setting and K with the highest silhouette
   (ties within 0.01: higher stability, then smaller K).
3. Among these winners select the highest silhouette; if winners are within
   0.02, take the most stable, then the simplest (K-means, hierarchical,
   spectral).
4. Checks, reported but not used to re-pick: (a) selected silhouette against
   a no-structure null (each feature permuted independently, 20+ times);
   (b) ARI between the selected clustering and the other winners.

If the checks show weak structure (null overlap, stability below ~0.6), say
so plainly.

## 4. Report: at most ONE printed page

**The report must fit on one printed letter page including all text, figures,
and tables. Present clustering results (assignments, plots, tables, cluster
summaries) for the ONE selected method only.** Other methods may be named
briefly, with at most their comparison score, to justify the selection; do
not show their clusterings.

Parts, in order:

1. **Data and goal** (2 sentences): n, p, preprocessing, seed.
2. **Methods and selection** (3-4 sentences): algorithms and grids, the
   criteria, the rule, and why the chosen method won, with its numbers.
3. **Figure** (one, two panels at most, about 6.5 x 2.7 in, 200+ dpi):
   (a) observations on the first two principal components, colored and
   marker-coded by selected cluster, axes labelled with % variance;
   (b) the most informative companion for the selected method: its silhouette
   plot, its dendrogram, or a heatmap of top cluster-separating features.
   Show supplied labels in (a) only as a secondary cue (marker fill or
   small text). Okabe-Ito colors, sentence-case titles, text at least 8 pt.
4. **Table** (one, small): cluster sizes, mean silhouette per cluster, and,
   if labels were supplied, the cluster x label counts.
5. **Interpretation** (3-4 bullets): what distinguishes the groups (features
   or components driving them), agreement with known labels if any (ARI,
   named exceptions), and the null and stability checks.
6. **Limitations** (2-3 bullets): e.g. small n, sensitivity to preprocessing
   and K, clusters are descriptive and not confirmed subtypes.

Style: plain words, no code, consistent rounding, no claims the numbers do
not support. Never change the method, K, or preprocessing after seeing how
clusters match the labels.

## 5. Verify before finishing

Render to PDF or self-contained HTML and check the page count: one page,
nothing clipped, all figure text readable. If it overflows, shorten text
first, then shrink the figure. Check every number in the text against the
script output. If asked to append the skill, put it after a page break; that
appendix is outside the limit.
