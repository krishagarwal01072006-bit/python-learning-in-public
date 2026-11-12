# Day 39, project 2: the leak - what happens when the test
# set is not really unseen. Run: python3 the_leak.py
# Same NBA 2017 file as project 1, same split, one difference:
# this script splits BEFORE removing the duplicate rows of
# traded players, so the same player lands on both sides.
import pandas as pd

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
print("Rows before dedupe:", len(nba))

# The mistake: split first, dedupe never.
train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)
leaked = sorted(set(train["Player"]) & set(test["Player"]))
print("Players on BOTH sides:", len(leaked))
print("Some of them:", leaked[:5])

# The fix: dedupe first, exactly like Day 37, then split.
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
train = nba.sample(frac=0.8, random_state=7)
test = nba.drop(train.index)
leaked = set(train["Player"]) & set(test["Player"])
print("\nAfter dedupe first:")
print("Train players:", len(train))
print("Test players:", len(test))
print("Players on BOTH sides:", len(leaked))
