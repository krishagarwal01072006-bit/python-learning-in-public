# Day 47, project 1: clustering - the Player Archetype Finder.
# Put the Kaggle file Seasons_Stats.csv (drgilermo/nba-players-stats)
# in this same folder, then run: python3 find_the_archetypes.py
# Uses pandas (Days 33/35), numpy (Days 29/31) and matplotlib
# (Day 31). New idea: k-means clustering. No labels, no right
# answer - the algorithm just groups players who look alike.
# Four per-game numbers define a player here: points, assists,
# rebounds and threes made. Per game, not season totals - season
# totals would group players by how many games they played.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]

# Dedupe FIRST (Day 37's lesson), then per-game numbers.
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.copy()
nba["PPG"] = nba["PTS"] / nba["G"]
nba["APG"] = nba["AST"] / nba["G"]
nba["RPG"] = nba["TRB"] / nba["G"]
nba["3PG"] = nba["3P"] / nba["G"]
print("Players:", len(nba))

features = ["PPG", "APG", "RPG", "3PG"]
data = nba[features].to_numpy(float)

# Standardise: subtract the mean, divide by the spread. Without
# this, points (0-32 a game) would drown out threes (0-4 a game)
# and the clusters would just be "scores a lot / scores a little".
mean = data.mean(axis=0)
spread = data.std(axis=0)
scaled = (data - mean) / spread

# K-means, written out by hand: pick 4 starting players at random,
# assign everyone to the nearest centre, move each centre to the
# middle of its group, repeat until nobody moves.
rng = np.random.default_rng(7)
centres = scaled[rng.choice(len(scaled), size=4, replace=False)]
for _ in range(100):
    distance = ((scaled[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
    group = distance.argmin(axis=1)
    new_centres = np.array([scaled[group == j].mean(axis=0) for j in range(4)])
    if np.allclose(new_centres, centres):
        break
    centres = new_centres

# Centres back in real per-game numbers, so they read like basketball.
real_centres = centres * spread + mean
names = ["Wings", "Bigs", "Bench", "Stars"]
print("\nThe four archetypes (centre = the average player in the group):")
for j in range(4):
    players = nba[group == j]
    top = players.sort_values("PPG", ascending=False)["Player"].head(3).tolist()
    print(f"{names[j]}: {len(players)} players - "
          f"{real_centres[j][0]:.1f} pts, {real_centres[j][1]:.1f} ast, "
          f"{real_centres[j][2]:.1f} reb, {real_centres[j][3]:.1f} threes a game")
    print(f"   Top scorers: {', '.join(top)}")

# Spot-check the famous names land where you would expect.
for star in ["Russell Westbrook", "Stephen Curry", "DeAndre Jordan",
             "Kyle Korver", "Chris Paul", "Hassan Whiteside"]:
    i = nba[nba["Player"] == star].index[0]
    pos = nba.index.get_loc(i)
    print(f"{star}: {names[group[pos]]}")

# Chart: points vs assists, coloured by archetype.
colours = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
for j in range(4):
    players = nba[group == j]
    plt.scatter(players["PPG"], players["APG"], s=12,
                color=colours[j], label=f"{names[j]} ({len(players)})")
plt.title("NBA 2017 player archetypes: points vs assists per game")
plt.xlabel("Points per game")
plt.ylabel("Assists per game")
plt.legend()
plt.savefig("nba_2017_archetypes.png")
print("\nChart saved: nba_2017_archetypes.png")
