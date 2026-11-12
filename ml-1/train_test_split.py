# Day 39, project 1: ML starts here - train/test split.
# Put the Kaggle file Seasons_Stats.csv (drgilermo/nba-players-stats)
# in this same folder, then run: python3 train_test_split.py
# Uses only pandas taught on Days 33 and 35, plus df.sample(),
# which this post introduces as the way to split a dataset.
# One idea: fit a simple rule on the training players, then measure
# it on test players the rule has never seen.
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]

# Traded players appear twice, so dedupe FIRST (Day 37's lesson).
# Splitting before this step puts the same player on both sides.
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
print("Players:", len(nba))

# Split: 80% train, 20% test. random_state=7 keeps the split
# the same every time you rerun the script.
train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)
print("Train players:", len(train))
print("Test players:", len(test))

# Fit: one number learned from the training players only,
# total points per minute played.
ratio = train["PTS"].sum() / train["MP"].sum()
print("Points per minute (learned from train):", round(ratio, 4))

# Predict: the rule guesses each test player's total points
# from minutes alone, then we measure how far off it was.
test = test.copy()
test["predicted"] = ratio * test["MP"]
test["error"] = (test["PTS"] - test["predicted"]).abs()
print("Test error (average miss):", round(test["error"].mean(), 1), "points")

# Same rule measured on the players it trained on.
train = train.copy()
train["predicted"] = ratio * train["MP"]
train_error = (train["PTS"] - train["predicted"]).abs().mean()
print("Train error (average miss):", round(train_error, 1), "points")

# Baseline: guess every test player scored the training average.
average = train["PTS"].mean()
baseline_error = (test["PTS"] - average).abs().mean()
print("Baseline error (just guess the average):", round(baseline_error, 1), "points")

# Where the rule misses worst: minutes alone cannot see talent.
worst = test.sort_values("error", ascending=False)
print("\nWorst miss:")
print(worst[["Player", "MP", "PTS", "predicted"]].head(1).to_string(index=False))

# Chart: actual points against predicted points for the test players.
test.plot(kind="scatter", x="predicted", y="PTS")
plt.title("Actual vs predicted points, NBA 2017 test players")
plt.xlabel("Predicted points")
plt.ylabel("Actual points")
plt.savefig("nba_2017_actual_vs_predicted.png")
print("\nChart saved: nba_2017_actual_vs_predicted.png")
