import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# run this from the pandas-2 folder, so read_csv finds messy.csv and cities.csv
scores = pd.read_csv("messy.csv").drop_duplicates().dropna()
cities = pd.read_csv("cities.csv")

# merge on the shared "name" key. Check dtypes first: a merge on
# mismatched key types (int vs str) fails outright with a ValueError.
print(scores.dtypes)
merged = scores.merge(cities, on="name")
print(merged)

by_city = merged.groupby("city")["score"].mean()
print(by_city)
by_city.plot(kind="bar")
plt.ylabel("mean score")
plt.title("mean score by city")
plt.savefig("mean_score_by_city.png")
print("chart saved: mean_score_by_city.png")
