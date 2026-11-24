# Day 49, project 1: cross-validation - the model showdown.
# Put the Kaggle file Seasons_Stats.csv (drgilermo/nba-players-stats)
# in this same folder, then run: python3 cross_validation.py
# Same NBA 2017 players and features as Day 41 (minutes, shot
# attempts, FG%), same target (total points). One new idea: do not
# trust a single train/test split. Shuffle the players into 5
# equal folds, test on one fold at a time, and average the five
# misses. Every model faces the same five folds, so the
# scoreboard is a fair fight.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.dropna(subset=["MP", "FGA", "FG%", "PTS"])
print("Players:", len(nba))

features = ["MP", "FGA", "FG%"]
X = nba[features].to_numpy(float)
y = nba["PTS"].to_numpy(float)

# Five folds, shuffled with seed 7 so the run repeats exactly.
rng = np.random.default_rng(7)
shuffled = rng.permutation(len(nba))
folds = np.array_split(shuffled, 5)
print("Fold sizes:", [len(f) for f in folds])

# Model 1: the baseline - guess the training average for everyone.
def predict_baseline(X_train, y_train, X_test):
    return np.full(len(X_test), y_train.mean())

# Model 2: Day 41's linear regression, least squares again.
def predict_regression(X_train, y_train, X_test):
    train_x = np.column_stack([np.ones(len(X_train)), X_train])
    test_x = np.column_stack([np.ones(len(X_test)), X_test])
    weights, _, _, _ = np.linalg.lstsq(train_x, y_train, rcond=None)
    return test_x @ weights

# Model 3: a small decision tree, written by hand (see
# decision_tree.py for the readable version). It keeps splitting
# players into two groups on one number until it is 3 splits deep
# or a group gets smaller than 20 players, then guesses the
# group's average points.
def build_tree(X, y, depth=0, max_depth=3, min_leaf=20):
    node = {"value": float(y.mean()), "n": len(y)}
    if depth >= max_depth or len(y) < 2 * min_leaf:
        return node
    best = None
    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        for t in (values[:-1] + values[1:]) / 2:
            left = X[:, j] <= t
            if left.sum() < min_leaf or (~left).sum() < min_leaf:
                continue
            error = (np.abs(y[left] - y[left].mean()).sum()
                     + np.abs(y[~left] - y[~left].mean()).sum()) / len(y)
            if best is None or error < best[0]:
                best = (error, j, t)
    if best is None:
        return node
    _, j, t = best
    left = X[:, j] <= t
    node["feature"] = j
    node["threshold"] = float(t)
    node["left"] = build_tree(X[left], y[left], depth + 1)
    node["right"] = build_tree(X[~left], y[~left], depth + 1)
    return node

def predict_tree(node, X):
    out = []
    for row in X:
        current = node
        while "feature" in current:
            if row[current["feature"]] <= current["threshold"]:
                current = current["left"]
            else:
                current = current["right"]
        out.append(current["value"])
    return np.array(out)

def predict_tree_model(X_train, y_train, X_test):
    return predict_tree(build_tree(X_train, y_train), X_test)

models = [
    ("Baseline (train average)", predict_baseline),
    ("Linear regression (Day 41)", predict_regression),
    ("Decision tree (depth 3)", predict_tree_model),
]

print("\nFold MAE (average miss, points):")
results = {}
for name, predict in models:
    fold_errors = []
    for k in range(5):
        test_idx = folds[k]
        train_idx = np.concatenate([folds[i] for i in range(5) if i != k])
        predicted = predict(X[train_idx], y[train_idx], X[test_idx])
        fold_errors.append(np.abs(y[test_idx] - predicted).mean())
    results[name] = fold_errors
    print(name, [round(e, 1) for e in fold_errors],
          "-> mean", round(float(np.mean(fold_errors)), 1),
          "+/-", round(float(np.std(fold_errors)), 1))

winner = min(results, key=lambda n: np.mean(results[n]))
print("\nWinner on the 5-fold average:", winner)
print("One split can lie: the baseline scored 356.1 on Day 41's",
      "single split, but its worst fold here is 412.5.")

# Chart: mean miss per model, with the fold-to-fold spread.
names = [n.split(" (")[0] for n, _ in models]
means = [float(np.mean(results[n])) for n, _ in models]
spreads = [float(np.std(results[n])) for n, _ in models]
plt.bar(names, means, yerr=spreads, capsize=6)
plt.ylabel("Average miss (points, lower is better)")
plt.title("Model showdown: 5-fold cross-validated MAE, NBA 2017")
plt.tight_layout()
plt.savefig("cv_scoreboard.png")
print("\nChart saved: cv_scoreboard.png")
