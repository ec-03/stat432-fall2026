---
name: lda-qda-report
description: Run a reproducible LDA/QDA classification analysis and write a one-page report. Use ONLY when I explicitly invoke this skill by name and supply the dataset, response, and predictors; never load it on your own.
disable-model-invocation: true
---

# LDA/QDA analysis with a one-page report

You are a careful statistician. The user supplies a data file, the response,
the predictors with their coding, and a random seed (pick and state one if
none is given). Do not drop, recode, or add variables beyond what is supplied.
Use Python (scikit-learn) or R (MASS); keep all code in one reproducible script.

## Candidate models (LDA/QDA family only)

1. **LDA** on the supplied predictors (empirical priors).
2. **QDA** on the supplied predictors (empirical priors).
3. **PCA + LDA** and **PCA + QDA**: standardize, project onto the first q
   principal components, then fit. Tune q over 1 to p (or a coarse grid if p
   is large).
4. **Blend**: P(k | x) = w P_LDA(k | x) + (1 - w) P_QDA(k | x), predicting
   the class with the largest blended probability. Tune w over
   {0, 0.1, ..., 1}; optionally blend the best PCA versions.

No other classifier families, no regularization, no tuning of the decision
threshold: predict the class with the largest posterior probability.

## Procedure (no leakage)

1. Set the seed once. Reserve a **stratified 25% test set** before any
   exploration, tuning, or plotting of the response. Do not touch it again
   until step 5.
2. Create **one stratified 10-fold split** of the training set and reuse the
   same folds for every candidate and every tuning value.
3. Fit all preprocessing (standardization, PCA) **inside each fold** on that
   fold's training part only (e.g. an sklearn `Pipeline`).
4. For each candidate record the mean CV misclassification rate and its
   standard error (SD of the 10 fold errors / sqrt(10)). Within each family
   keep the tuning value with the lowest mean CV error (ties: smaller q, or w
   closer to 0 or 1). Select the candidate with the lowest mean CV error
   overall (ties: the one with fewer parameters, LDA < QDA). Do not apply a
   one-SE rule; instead flag in the table every candidate within one SE of
   the selected one, since those are not clearly worse.
5. Refit the selected model and its preprocessing on the **full training
   set**, then evaluate it **once** on the test set. Report the test
   misclassification rate, a 95% Wilson interval, and the test confusion
   matrix (observed in rows, predicted in columns).
6. Also report the majority-class (no-information) error on the test set and
   the test errors of plain LDA and QDA refit on the full training set as
   reference points, clearly labelled as not used for selection.

Sanity checks before writing: class counts per fold, no missing values,
covariance matrices non-singular (report if QDA warns), selected setting
lies inside its grid (widen the grid if it sits on an edge that can grow).

## Report (at most ONE printed letter page, render and check)

Title, then these short parts, in this order:

1. **Data and goal** (2-3 sentences): n, number of predictors, class
   proportions, split sizes, seed.
2. **Candidates and CV** (2-3 sentences): models, grids, fold scheme,
   selection rule.
3. **Figure** (one, ~6.5 x 2.6 in, 200+ dpi): mean CV error (y, "CV
   misclassification rate") against the tuning parameter (x), one panel per
   tuned family (PCA q; blend weight w), with +/-1 SE bars; draw plain LDA
   and QDA CV errors as labelled horizontal reference lines and mark the
   selected point. Okabe-Ito colors with distinct markers/line styles,
   sentence-case titles, all text >= 9 pt, no top/right spines.
4. **Table** (one): each candidate at its best setting with columns
   *Model, Setting, CV error, SE, Within 1 SE*, sorted by CV error, the
   selected row in bold. Round errors to 3 decimals.
5. **Selected model and test result**: one sentence naming the model and
   setting, then test error (95% CI), the 2x2 (or KxK) test confusion matrix,
   and the reference errors from step 6.
6. **Findings and limitations** (3-5 bullets): what drives performance
   (e.g. shared vs. separate covariance, dimension reduction), how close the
   candidates are relative to their SEs, and limitations (single split, small
   test set, normality, selection noise, threshold 0.5 ignores costs).

Style: plain words, no code in the report, numbers with consistent rounding,
no claims that the numbers do not support. Never revise the model, grid, or
text in response to the test result. After rendering, confirm the report fits
on one page; if not, shorten text first, then shrink the figure.
