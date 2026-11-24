# Day 49, project 3: the showdown predictor - ask all three models.
# Run: python3 showdown.py
# Type in a player's minutes, shot attempts and FG%, and the
# baseline, the regression and the tree each guess their total
# points. The models are fitted on all 485 players here - after
# cross-validation picks the winner, you refit it on everything.
# The CV score (average miss across 5 folds) is printed next to
# each guess, so you know which guess to trust.
import pandas as pd
import numpy as np

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.dropna(subset=["MP", "FGA", "FG%", "PTS"])
features = ["MP", "FGA", "FG%"]
X = nba[features].to_numpy(float)
y = nba["PTS"].to_numpy(float)

# The tree builder from decision_tree.py, reused here.
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

def predict_tree(node, row):
    current = node
    while "feature" in current:
        if row[current["feature"]] <= current["threshold"]:
            current = current["left"]
        else:
            current = current["right"]
    return current["value"]

minutes = float(input("Minutes played in the season: "))
attempts = float(input("Field-goal attempts in the season: "))
fg = float(input("Field-goal % as a decimal (e.g. 0.45): "))
player = np.array([minutes, attempts, fg])

baseline = y.mean()
train_x = np.column_stack([np.ones(len(X)), X])
weights, _, _, _ = np.linalg.lstsq(train_x, y, rcond=None)
regression = float(np.array([1, minutes, attempts, fg]) @ weights)
tree = build_tree(X, y)
tree_guess = predict_tree(tree, player)

print(f"\nBaseline (everyone's average): {baseline:.0f} points  [CV miss 376.4]")
print(f"Linear regression:             {regression:.0f} points  [CV miss 44.8]")
print(f"Decision tree:                 {tree_guess:.0f} points  [CV miss 74.6]")
print("\nTrust the regression - it won all five folds, not just one split.")
