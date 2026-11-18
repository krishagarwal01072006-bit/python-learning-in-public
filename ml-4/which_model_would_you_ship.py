# Day 45, project 3: which model would you ship?
# Run: python3 which_model_would_you_ship.py
# Type in an app's numbers and two models answer side by side:
# Day 43's honest 5-feature model (trained on all 7,114 apps)
# and the overfit 25-feature model (trained on only 100 apps).
# They agree on easy apps and disagree on weird ones - and the
# overfit one is always more sure of itself. That confidence is
# the tell: it memorised 100 apps, it did not learn the pattern.
import pandas as pd
import numpy as np

df = pd.read_csv("googleplaystore.csv")
df = df.drop_duplicates().dropna(subset=["Rating"])
df["Installs"] = pd.to_numeric(df["Installs"].str.replace("+", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
df["Price"] = pd.to_numeric(df["Price"].str.replace("$", "", regex=False), errors="coerce")
df["Size_MB"] = pd.to_numeric(df["Size"].str.replace("M", "", regex=False), errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df = df.dropna(subset=["Installs", "Price", "Reviews"])
df["Size_MB"] = df["Size_MB"].fillna(df["Size_MB"].median())

df["hit"] = (df["Rating"] >= 4.2).astype(int)
df["log_reviews"] = np.log1p(df["Reviews"])
df["log_installs"] = np.log1p(df["Installs"])
df["is_free"] = (df["Type"] == "Free").astype(int)

train = df.sample(frac=0.8, random_state=7)
base = ["log_reviews", "log_installs", "Price", "Size_MB", "is_free"]

def expand(data):
    cols = {c: data[c].values.astype(float) for c in base}
    out = dict(cols)
    for c in base:
        out[c + "^2"] = cols[c] ** 2
        out[c + "^3"] = cols[c] ** 3
    for i in range(len(base)):
        for j in range(i + 1, len(base)):
            out[base[i] + "*" + base[j]] = cols[base[i]] * cols[base[j]]
    return pd.DataFrame(out, index=data.index)

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def fit(features, n_train, steps):
    tr = train if n_train is None else train.sample(n=n_train, random_state=7)
    trd = expand(tr) if features == "fancy" else tr[base].copy()
    mu, sd = trd.mean(), trd.std().replace(0, 1)
    train_x = np.column_stack([np.ones(len(trd))] + [((trd[c] - mu[c]) / sd[c]).values for c in trd.columns])
    train_y = tr["hit"].values.astype(float)
    weights = np.zeros(train_x.shape[1])
    for step in range(steps):
        prob = sigmoid(train_x @ weights)
        weights -= 0.1 * (train_x.T @ (prob - train_y)) / len(train_y)
    return weights, mu, sd

# Honest model: 5 features, all 7,114 training apps, 2,000 steps.
simple_w, simple_mu, simple_sd = fit("simple", None, 2000)
# Overfit model: 25 features, 100 training apps, 10,000 steps.
fancy_w, fancy_mu, fancy_sd = fit("fancy", 100, 10000)

def predict(row):
    # row: one app as a small table with the 5 base features.
    simple_x = np.array([1] + [((float(row[c].iloc[0]) - simple_mu[c]) / simple_sd[c]) for c in base])
    fancy_row = expand(row)
    fancy_x = np.array([1] + [((fancy_row[c].iloc[0] - fancy_mu[c]) / fancy_sd[c]) for c in fancy_row.columns])
    return float(sigmoid(simple_x @ simple_w)), float(sigmoid(fancy_x @ fancy_w))

def show(name, row, rating):
    simple_p, fancy_p = predict(row)
    print(f"{name} (rated {rating}): honest model {simple_p * 100:.1f}% hit, overfit model {fancy_p * 100:.1f}% hit")

# Reality checks: real apps from the dataset, same three Day 43 used.
for app_name in ["Clash of Clans", "I'm Rich - Trump Edition", "Las Vegas Lights FC"]:
    row = df[df["App"] == app_name].iloc[[0]][base + ["Rating"]]
    show(app_name, row[base], round(float(row["Rating"].iloc[0]), 1))

print("\nNow try your own app.")
reviews = float(input("How many reviews does it have? "))
installs = float(input("How many installs? "))
price = float(input("Price in dollars (0 if free)? "))
size = float(input("Size in MB? "))
free = input("Is it free? (yes/no) ").strip().lower() == "yes"
row = pd.DataFrame([{"log_reviews": np.log1p(reviews), "log_installs": np.log1p(installs),
                    "Price": price, "Size_MB": size, "is_free": 1 if free else 0}])
simple_p, fancy_p = predict(row)
print(f"\nHonest model: {simple_p * 100:.1f}% chance of being a hit.")
print(f"Overfit model: {fancy_p * 100:.1f}% chance of being a hit.")
if abs(simple_p - fancy_p) > 0.2:
    print("They disagree by a lot. The overfit one is guessing from")
    print("100 memorised apps - trust the honest one.")
else:
    print("They agree here. Las Vegas Lights FC above already split")
    print("them by 18 points - try a weirder app and watch it happen again.")
