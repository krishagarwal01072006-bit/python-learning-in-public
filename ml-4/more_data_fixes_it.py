# Day 45, project 2: more data fixes it.
# Run: python3 more_data_fixes_it.py
# The same 25-feature model from project 1, trained on 100, 300,
# 1,000 and then all 7,114 training apps. Same test apps every
# time (1,778), same 10,000 steps. One idea: memorising is only
# possible when the model has more knobs than examples. Give it
# enough examples and the same complicated model has to learn
# the real pattern instead.
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
print("Apps after cleaning:", len(df))

df["hit"] = (df["Rating"] >= 4.2).astype(int)
df["log_reviews"] = np.log1p(df["Reviews"])
df["log_installs"] = np.log1p(df["Installs"])
df["is_free"] = (df["Type"] == "Free").astype(int)

train = df.sample(frac=0.8, random_state=7)
test = df.drop(train.index)

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

test_expanded = expand(test)
test_y = test["hit"].values.astype(int)

for n_train in [100, 300, 1000, 7114]:
    tr = train.sample(n=n_train, random_state=7)
    trd = expand(tr)
    mu, sd = trd.mean(), trd.std().replace(0, 1)
    def make_x(data):
        return np.column_stack([np.ones(len(data))] + [((data[c] - mu[c]) / sd[c]).values for c in data.columns])
    train_x, test_x = make_x(trd), make_x(test_expanded)
    train_y = tr["hit"].values.astype(float)
    weights = np.zeros(train_x.shape[1])
    for step in range(10000):
        prob = sigmoid(train_x @ weights)
        weights -= 0.1 * (train_x.T @ (prob - train_y)) / len(train_y)
    train_acc = ((sigmoid(train_x @ weights) >= 0.5).astype(int) == train_y).mean() * 100
    test_acc = ((sigmoid(test_x @ weights) >= 0.5).astype(int) == test_y).mean() * 100
    print(f"25-feature model, {n_train} training apps: train {train_acc:.1f}%  test {test_acc:.1f}%  gap {train_acc - test_acc:.1f} points")

print("\nSame model, same test apps. Only the training size changed,")
print("and the gap closes as the data grows. More data is the fix")
print("that needs no new maths at all.")
