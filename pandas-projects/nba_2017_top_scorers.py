# Day 37, project 2: NBA 2017 season analysis.
# Put the Kaggle file Seasons_Stats.csv (drgilermo/nba-players-stats)
# in this same folder, then run: python3 nba_2017_top_scorers.py
# Uses only pandas taught on Days 33 and 35: read_csv, filtering,
# sort_values, drop_duplicates, groupby + agg, df.plot().
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Seasons_Stats.csv")
nba_2017 = df[df["Year"] == 2017]
print("2017 rows at the start:", len(nba_2017))

# Traded players appear twice: once per team, plus a TOT full-season row.
# Keep the row with the most games played, which is the full-season row.
nba_2017 = nba_2017.sort_values("G", ascending=False)
nba_2017 = nba_2017.drop_duplicates(subset=["Player"])
print("Players after keeping one row each:", len(nba_2017))

# Krish's own questions:
# 1. Who scored the most total points in 2017?
print("\nTop 10 scorers by total points:")
print(nba_2017.sort_values("PTS", ascending=False)[["Player", "Pos", "Tm", "G", "PTS"]].head(10))

# 2. Who scored most per game, counting only players with 50+ games,
# so a one-game cameo cannot top the list?
nba_2017["PPG"] = nba_2017["PTS"] / nba_2017["G"]
regulars = nba_2017[nba_2017["G"] >= 50]
print("\nTop 10 scorers by points per game (50+ games):")
print(regulars.sort_values("PPG", ascending=False)[["Player", "Pos", "Tm", "G", "PPG"]].head(10))

# 3. Which position scores most on average?
print("\nAverage total points by position:")
print(nba_2017.groupby("Pos")["PTS"].mean().sort_values(ascending=False))

# 4. Chart the top scorers, with the one-line plot from Day 35.
top = nba_2017.sort_values("PTS", ascending=False).head(10)
top.plot(kind="bar", x="Player", y="PTS", legend=False)
plt.title("Top 10 scorers, NBA 2017")
plt.ylabel("Total points")
plt.savefig("nba_2017_top_scorers.png")
print("\nChart saved: nba_2017_top_scorers.png")
