# Day 41, project 2: one number vs three numbers.
# Run: python3 one_vs_three.py
# Same NBA 2017 players, same split as Day 39 (random_state=7),
# three models side by side so the improvement is honest:
# the Day 39 dumb rule, minutes + shot attempts, and the full
# three-feature regression. FG% is what turns attempts into
# points, so it earns its place last.
import pandas as pd
import numpy as np

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.dropna(subset=["MP", "FGA", "FG%", "PTS"])

train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)

# Model 1: the Day 39 dumb rule - one ratio learned from train.
ratio = train["PTS"].sum() / train["MP"].sum()
error_1 = (test["PTS"] - ratio * test["MP"]).abs().mean()
print("1. Dumb rule (minutes only): test error", round(error_1, 1))

# Model 2 and 3: least squares with two, then three features.
def test_error_for(features):
    train_x = np.column_stack([np.ones(len(train))] + [train[c] for c in features])
    test_x = np.column_stack([np.ones(len(test))] + [test[c] for c in features])
    weights, _, _, _ = np.linalg.lstsq(train_x, train["PTS"], rcond=None)
    predicted = test_x @ weights
    return (test["PTS"] - predicted).abs().mean(), weights

error_2, weights_2 = test_error_for(["MP", "FGA"])
print("2. Minutes + shot attempts: test error", round(error_2, 1))
print("   Weights (intercept, MP, FGA):", np.round(weights_2, 2))

error_3, weights_3 = test_error_for(["MP", "FGA", "FG%"])
print("3. Minutes + attempts + FG%: test error", round(error_3, 1))
print("   Weights (intercept, MP, FGA, FG%):", np.round(weights_3, 2))

print("\nImprovement, dumb rule to full model:",
      round(error_1 - error_3, 1), "points per player")
print("Minutes weight in model 3 is near zero:", round(weights_3[1], 3))
print("Once shots are in the model, minutes stop adding anything.")
