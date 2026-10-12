# Q4: LDA/QDA analysis of SAheart, following SKILL.md (lda-qda-report)
import numpy as np, pandas as pd
from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis as LDA,
                                           QuadraticDiscriminantAnalysis as QDA)
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

heart = pd.read_csv("data/saheart.csv")
heart["famhist"] = heart["famhist"].map({"Absent": 1, "Present": 2})
X = heart.drop(columns="chd").to_numpy(); y = heart["chd"].to_numpy()
SEED = 432
# 1. Reserve a stratified 25% test set before anything else
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y,
                                      random_state=SEED)
# 2. One stratified 10-fold split, reused for every candidate
folds = list(StratifiedKFold(10, shuffle=True, random_state=SEED).split(Xtr, ytr))
assert all(np.bincount(ytr[va]).min() > 0 for _, va in folds)

def pca_model(q, base):  # 3. scaling + PCA are fitted inside each fold
    return lambda: make_pipeline(StandardScaler(), PCA(q), base())

def cv_probs(make):
    return [make().fit(Xtr[t], ytr[t]).predict_proba(Xtr[v])[:, 1] for t, v in folds]

def cv_error(P):  # 4. mean CV misclassification rate and its SE
    e = np.array([np.mean((p > 0.5) != ytr[v]) for p, (_, v) in zip(P, folds)])
    return e.mean(), e.std(ddof=1) / np.sqrt(len(folds))

p = X.shape[1]; qs = range(1, p + 1); ws = np.round(np.linspace(0, 1, 11), 1)
P_lda, P_qda = cv_probs(LDA), cv_probs(QDA)
cv = {"LDA": {None: cv_error(P_lda)}, "QDA": {None: cv_error(P_qda)},
      "PCA + LDA": {q: cv_error(cv_probs(pca_model(q, LDA))) for q in qs},
      "PCA + QDA": {q: cv_error(cv_probs(pca_model(q, QDA))) for q in qs},
      "Blend": {w: cv_error([w * a + (1 - w) * b for a, b in zip(P_lda, P_qda)])
                for w in ws}}

def best(fam):  # lowest CV error; ties -> smaller q, or w nearer 0 or 1
    tie = (lambda s: s) if fam.startswith("PCA") else (lambda s: -abs(s - 0.5))
    return min(cv[fam], key=lambda s: (round(cv[fam][s][0], 10),
                                       0 if s is None else tie(s)))

nparam = {"LDA": 1, "PCA + LDA": 1, "QDA": 2, "PCA + QDA": 2, "Blend": 3}
rows = [(f, best(f), *cv[f][best(f)]) for f in cv]
table = pd.DataFrame(rows, columns=["Model", "Setting", "CV error", "SE"])
table = table.assign(k=table["Model"].map(nparam)).sort_values(
    ["CV error", "k"]).drop(columns="k").reset_index(drop=True)
sel = table.iloc[0]
table["Within 1 SE"] = np.where(table.index == 0, "selected",
    np.where(table["CV error"] <= sel["CV error"] + sel["SE"], "yes", "no"))

# 5. Refit the selected model on all training data; evaluate once on the test set
class Blend:  # w * P_LDA + (1 - w) * P_QDA
    def __init__(self, w): self.w, self.m = w, (LDA(), QDA())
    def fit(self, X, y): [m.fit(X, y) for m in self.m]; return self
    def predict(self, X):
        P = self.w * self.m[0].predict_proba(X) + (1 - self.w) * self.m[1].predict_proba(X)
        return self.m[0].classes_[P.argmax(1)]

def make_final(model, s):
    if model.startswith("PCA"):
        return pca_model(int(s), LDA if model.endswith("LDA") else QDA)()
    return Blend(s) if model == "Blend" else (LDA if model == "LDA" else QDA)()

final = make_final(sel["Model"], sel["Setting"]).fit(Xtr, ytr)
pred = final.predict(Xte); n_te = len(yte); err = np.mean(pred != yte)
z = 1.96; c = (err + z**2 / (2 * n_te)) / (1 + z**2 / n_te)
h = z * np.sqrt(err * (1 - err) / n_te + z**2 / (4 * n_te**2)) / (1 + z**2 / n_te)
ci = (c - h, c + h)                                 # 95% Wilson interval
cm = confusion_matrix(yte, pred)
# 6. Reference points (not used for selection)
ref = {"Majority class": np.mean(yte != np.bincount(ytr).argmax()),
       "LDA": np.mean(LDA().fit(Xtr, ytr).predict(Xte) != yte),
       "QDA": np.mean(QDA().fit(Xtr, ytr).predict(Xte) != yte)}
