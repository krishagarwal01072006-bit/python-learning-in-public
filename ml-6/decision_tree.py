# Day 49, project 2: a decision tree, written by hand.
# Run: python3 decision_tree.py
# Same NBA 2017 players and Day 41 split (80% train, 20% test,
# random_state=7) so the numbers compare directly with Day 41.
# One new trick: build_tree calls itself. A function calling
# itself is called recursion - each call handles one smaller
# group of players until the group is too small to split.
import pandas as pd
import numpy as np

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.dropna(subset=["MP", "FGA", "FG%", "PTS"])

train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)
features = ["MP", "FGA", "FG%"]
X_train = train[features].to_numpy(float)
y_train = train["PTS"].to_numpy(float)
X_test = test[features].to_numpy(float)
y_test = test["PTS"].to_numpy(float)

def build_tree(X, y, depth=0, max_depth=3, min_leaf=20):
    # A leaf just guesses its group's average points.
    node = {"value": float(y.mean()), "n": len(y)}
    if depth >= max_depth or len(y) < 2 * min_leaf:
        return node
    # Try every feature and every midpoint split; keep the split
    # whose two groups have the smallest average miss.
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
    node["feature"] = features[j]
    node["threshold"] = float(t)
    node["left"] = build_tree(X[left], y[left], depth + 1)
    node["right"] = build_tree(X[~left], y[~left], depth + 1)
    return node

def show(node, indent=0):
    if "feature" in node:
        print(" " * indent + f"if {node['feature']} <= {node['threshold']:.1f}:")
        show(node["left"], indent + 2)
        print(" " * indent + "else:")
        show(node["right"], indent + 2)
    else:
        print(" " * indent + f"guess {node['value']:.0f} points ({node['n']} players)")

def predict(node, X):
    out = []
    for row in X:
        current = node
        while "feature" in current:
            j = features.index(current["feature"])
            if row[j] <= current["threshold"]:
                current = current["left"]
            else:
                current = current["right"]
        out.append(current["value"])
    return np.array(out)

tree = build_tree(X_train, y_train)
print("The tree the model learned (train players only):")
show(tree)
train_error = np.abs(y_train - predict(tree, X_train)).mean()
test_error = np.abs(y_test - predict(tree, X_test)).mean()
print("\nTrain error (average miss):", round(float(train_error), 1), "points")
print("Test error (average miss):", round(float(test_error), 1), "points")
print("Day 41 regression on this same split: 40.8.")
print("The tree only ever splits on shot attempts - it never",
      "touches minutes or FG%. Attempts carry the signal, but",
      "binning players into flat groups still loses to a line.")
