# Day 47, project 3: which archetype am I?
# Run: python3 which_archetype_am_i.py
# Same four centres as find_the_archetypes.py. Type in any player's
# per-game line and it tells you the nearest archetype and how far
# away you are. Try a real one: Westbrook 31.6 pts, 10.4 ast,
# 10.7 reb, 2.5 threes. Or DeAndre Jordan: 12.7, 1.2, 13.8, 0.0.
import pandas as pd
import numpy as np

df = pd.read_csv("Seasons_Stats.csv")
nba = df[df["Year"] == 2017]
nba = nba.sort_values("G", ascending=False)
nba = nba.drop_duplicates(subset=["Player"])
nba = nba.copy()
nba["PPG"] = nba["PTS"] / nba["G"]
nba["APG"] = nba["AST"] / nba["G"]
nba["RPG"] = nba["TRB"] / nba["G"]
nba["3PG"] = nba["3P"] / nba["G"]

features = ["PPG", "APG", "RPG", "3PG"]
data = nba[features].to_numpy(float)
mean = data.mean(axis=0)
spread = data.std(axis=0)
scaled = (data - mean) / spread

rng = np.random.default_rng(7)
centres = scaled[rng.choice(len(scaled), size=4, replace=False)]
for _ in range(100):
    distance = ((scaled[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
    group = distance.argmin(axis=1)
    new_centres = np.array([scaled[group == j].mean(axis=0) for j in range(4)])
    if np.allclose(new_centres, centres):
        break
    centres = new_centres

names = ["Wings", "Bigs", "Bench", "Stars"]
real_centres = centres * spread + mean

print("Four archetypes, NBA 2017 (per game):")
for j in range(4):
    print(f"  {names[j]}: {real_centres[j][0]:.1f} pts, "
          f"{real_centres[j][1]:.1f} ast, {real_centres[j][2]:.1f} reb, "
          f"{real_centres[j][3]:.1f} threes")

print("\nType a per-game line and I will place it.")
ppg = float(input("Points per game: "))
apg = float(input("Assists per game: "))
rpg = float(input("Rebounds per game: "))
threes = float(input("Threes made per game: "))
player = np.array([ppg, apg, rpg, threes])
player_scaled = (player - mean) / spread
gaps = np.sqrt(((centres - player_scaled) ** 2).sum(axis=1))
nearest = int(gaps.argmin())
print(f"\nThat is a {names[nearest]}: {gaps[nearest]:.2f} away from the "
      f"{names[nearest]} centre.")
print("Distances to all four centres:")
for j in range(4):
    print(f"  {names[j]}: {gaps[j]:.2f}")
