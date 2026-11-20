# Day 47, project 2: how many clusters? The elbow test.
# Run: python3 how_many_clusters.py
# Same players and features as find_the_archetypes.py, but run
# k-means for k = 1 to 8 and print how tight each answer is.
# Tightness is WCSS: add up every player's squared distance to
# their own centre. More clusters always means a smaller number,
# so the question is where the drops stop being worth it.
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
scaled = (data - data.mean(axis=0)) / data.std(axis=0)


def run_kmeans(k):
    rng = np.random.default_rng(7)
    centres = scaled[rng.choice(len(scaled), size=k, replace=False)]
    for _ in range(100):
        distance = ((scaled[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
        group = distance.argmin(axis=1)
        new_centres = np.array([scaled[group == j].mean(axis=0)
                                for j in range(k)])
        if np.allclose(new_centres, centres):
            break
        centres = new_centres
    tightness = ((scaled - centres[group]) ** 2).sum()
    return tightness


print("k = clusters, WCSS = how spread out the groups still are:")
last = None
for k in range(1, 9):
    score = run_kmeans(k)
    drop = "" if last is None else f" (down {last - score:.1f})"
    print(f"k={k}: WCSS {score:.1f}{drop}")
    last = score
print("\nNo sharp elbow: the drops shrink after k=4, they never stop.")
print("So k=4 is a choice I defend (four groups that read like real")
print("basketball roles), not a number the data handed me.")
