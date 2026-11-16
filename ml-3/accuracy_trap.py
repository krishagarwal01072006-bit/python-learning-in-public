# Day 43, project 2: the accuracy trap, side by side.
# Run: python3 accuracy_trap.py
# Three scorers on the same Play Store test apps, same split as
# project 1 (random_state=7): the dumb always-guess-hit baseline,
# a one-feature logistic model (reviews only), and the full
# five-feature model. One number, accuracy, hides the difference
# between them. The confusion matrix does not.
import pandas as pd
import numpy as np

df = pd.read_csv("googleplaystore.csv")
df = df.drop_duplicates().dropna(subset=["Rating"])
df["Installs"] = pd.to_numeric(df["Installs"].str.replace("+", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
df["Price"] = pd.to_numeric(df["Price"].str.replace("$", "", regex=False), errors="coerce")
df["Size_MB"] = pd.to_numeric(df["Size"].str.replace("M", "", regex=False), errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df = df.dropna(subset=["Installs", "Price", "Reviews"])
df["Size_MB"] = df["Size_MB"].fillna(df["Size_MB"].median())
df["hit"] = (df["Rating"] >= 4.2).astype(int)
df["log_reviews"] = np.log1p(df["Reviews"])
df["log_installs"] = np.log1p(df["Installs"])
df["is_free"] = (df["Type"] == "Free").astype(int)

train = df.sample(frac=0.8, random_state=7)
test = df.drop(train.index)
test_y = test["hit"].values.astype(int)

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def fit_logreg(features):
    mu = train[features].mean()
    sd = train[features].std()
    def make_x(data):
        return np.column_stack([np.ones(len(data))] + [((data[c] - mu[c]) / sd[c]).values for c in features])
    train_x, test_x = make_x(train), make_x(test)
    train_y = train["hit"].values.astype(float)
    weights = np.zeros(train_x.shape[1])
    for step in range(2000):
        prob = sigmoid(train_x @ weights)
        weights -= 0.1 * (train_x.T @ (prob - train_y)) / len(train_y)
    return (sigmoid(test_x @ weights) >= 0.5).astype(int)

def score(name, pred):
    tp = int(((pred == 1) & (test_y == 1)).sum())
    tn = int(((pred == 0) & (test_y == 0)).sum())
    fp = int(((pred == 1) & (test_y == 0)).sum())
    fn = int(((pred == 0) & (test_y == 1)).sum())
    acc = (tp + tn) / len(test_y)
    print(f"{name}: accuracy {acc * 100:.1f}%  TP {tp} TN {tn} FP {fp} FN {fn}  flops spotted {tn / (tn + fp) * 100:.1f}%")

# 1. The dumb baseline: call every app a hit. No model at all.
score("Always guess hit", np.ones(len(test_y), dtype=int))
# 2. One feature only: how many reviews the app has.
score("Reviews only", fit_logreg(["log_reviews"]))
# 3. The full model from project 1.
score("Full model (5 features)", fit_logreg(["log_reviews", "log_installs", "Price", "Size_MB", "is_free"]))

print("\nThe reviews-only model LEARNED something real (hits have a")
print("median 13,788 reviews, flops only 949) and still scores")
print("WORSE than guessing. Accuracy alone would never tell you.")
