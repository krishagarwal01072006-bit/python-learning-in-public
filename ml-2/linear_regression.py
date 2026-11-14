# Day 41, project 1: linear regression - Beat The Dumb Rule v2.
# Put the Kaggle file Seasons_Stats.csv (drgilermo/nba-players-stats)
# in this same folder, then run: python3 linear_regression.py
# Uses pandas (Days 33/35), numpy lstsq (new here: least squares
# fits the line that minimises squared error), and the Day 39
# train/test split. One idea: give the model three numbers
# instead of one, and let it learn a weight for each.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]

# Dedupe FIRST (Day 37's lesson), then drop the one player
# with no FG% so every feature exists for every player.
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.dropna(subset=["MP", "FGA", "FG%", "PTS"])
print("Players:", len(nba))

# Same split as Day 39: 80% train, 20% test, random_state=7.
train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)
print("Train players:", len(train))
print("Test players:", len(test))

# Features: minutes, field-goal attempts, field-goal %.
# The column of ones is the intercept - the model's starting point.
features = ["MP", "FGA", "FG%"]
train_x = np.column_stack([np.ones(len(train))] + [train[c] for c in features])
test_x = np.column_stack([np.ones(len(test))] + [test[c] for c in features])

# Fit: least squares learns one weight per feature, from train only.
weights, _, _, _ = np.linalg.lstsq(train_x, train["PTS"], rcond=None)
print("Weights (intercept, MP, FGA, FG%):", np.round(weights, 2))

# Predict on both sides, measure the average miss (MAE).
train = train.copy()
test = test.copy()
train["predicted"] = train_x @ weights
test["predicted"] = test_x @ weights
train_error = (train["PTS"] - train["predicted"]).abs().mean()
test_error = (test["PTS"] - test["predicted"]).abs().mean()
print("Train error (average miss):", round(train_error, 1), "points")
print("Test error (average miss):", round(test_error, 1), "points")
print("Day 39 dumb rule missed by 135.0 on the test players.")

# Where it still misses worst: even three numbers cannot see talent.
worst = test.copy()
worst["error"] = (worst["PTS"] - worst["predicted"]).abs()
worst = worst.sort_values("error", ascending=False)
print("\nWorst miss:")
print(worst[["Player", "MP", "FGA", "FG%", "PTS", "predicted"]].head(1).to_string(index=False))

# Chart: actual points against predicted points for the test players.
test.plot(kind="scatter", x="predicted", y="PTS")
plt.title("Actual vs predicted points, NBA 2017 test players (3 features)")
plt.xlabel("Predicted points")
plt.ylabel("Actual points")
plt.savefig("nba_2017_actual_vs_predicted_3features.png")
print("\nChart saved: nba_2017_actual_vs_predicted_3features.png")
