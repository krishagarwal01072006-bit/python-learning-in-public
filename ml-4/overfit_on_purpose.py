# Day 45, project 1: overfitting - make it worse on purpose.
# Run: python3 overfit_on_purpose.py
# Same Play Store data and split as Day 43 (random_state=7):
# 8,892 apps after cleaning, 7,114 train / 1,778 test, and a hit
# is an app rated 4.2 stars or more. Day 43's honest model scored
# 67.2% on the test apps. Today I break it on purpose, two ways:
# give it too many features, and starve it of data. Then I fix it.
# One idea: a model can memorise its training apps instead of
# learning what makes an app a hit - and train accuracy is the
# number that lies to you about it.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("googleplaystore.csv")
df = df.drop_duplicates().dropna(subset=["Rating"])
# Same cleaning as Day 37: "1,000,000+" installs, "$2.99" prices,
# "19M" sizes, and the corrupt "Free" row that crashed Day 37 with:
# ValueError: Unable to parse string "Free" at position 8644
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
print("Train apps:", len(train), " Test apps:", len(test))

base = ["log_reviews", "log_installs", "Price", "Size_MB", "is_free"]

def expand(data):
    # 25 features from 5: each feature, its square, its cube,
    # and every pair multiplied together. More knobs to turn
    # means more room to memorise instead of learn.
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

def fit_and_score(name, features, n_train, steps):
    # features: "simple" (5) or "fancy" (25). n_train: how many
    # apps the model is allowed to learn from.
    tr = train if n_train is None else train.sample(n=n_train, random_state=7)
    trd = expand(tr) if features == "fancy" else tr[base].copy()
    ted = expand(test) if features == "fancy" else test[base].copy()
    mu, sd = trd.mean(), trd.std().replace(0, 1)
    def make_x(data):
        return np.column_stack([np.ones(len(data))] + [((data[c] - mu[c]) / sd[c]).values for c in data.columns])
    train_x, test_x = make_x(trd), make_x(ted)
    train_y = tr["hit"].values.astype(float)
    test_y = test["hit"].values.astype(int)
    weights = np.zeros(train_x.shape[1])
    for step in range(steps):
        prob = sigmoid(train_x @ weights)
        weights -= 0.1 * (train_x.T @ (prob - train_y)) / len(train_y)
    train_acc = ((sigmoid(train_x @ weights) >= 0.5).astype(int) == train_y).mean() * 100
    test_acc = ((sigmoid(test_x @ weights) >= 0.5).astype(int) == test_y).mean() * 100
    print(f"{name}: train {train_acc:.1f}%  test {test_acc:.1f}%  gap {train_acc - test_acc:.1f} points")
    return train_acc, test_acc

results = {}
# 1. Day 43's honest model: 5 features, all 7,114 training apps.
results["Simple\n5 features\n7,114 apps"] = fit_and_score("1. Simple model, full data", "simple", None, 2000)
# 2. The sabotage: 25 features, only 100 training apps, and ten
# thousand steps to really let it memorise them.
results["Overfit\n25 features\n100 apps"] = fit_and_score("2. Overfit on purpose", "fancy", 100, 10000)
# 3. Fix one, more data: the same 25-feature model, all 7,114 apps.
results["Fixed: more data\n25 features\n7,114 apps"] = fit_and_score("3. Same fancy model, full data", "fancy", None, 10000)
# 4. Fix two, fewer features: the simple model, only 100 apps.
results["Fixed: fewer features\n5 features\n100 apps"] = fit_and_score("4. Simple model, 100 apps", "simple", 100, 2000)

print("\nTrain accuracy is the liar: the overfit model looks best")
print("on the apps it trained on, and worst where it counts.")

# Chart: train vs test bars, so the split-apart gap is visible.
names = list(results.keys())
train_scores = [v[0] for v in results.values()]
test_scores = [v[1] for v in results.values()]
x = np.arange(len(names))
plt.bar(x - 0.2, train_scores, 0.4, label="Train accuracy")
plt.bar(x + 0.2, test_scores, 0.4, label="Test accuracy")
plt.xticks(x, names)
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.title("Overfitting: train and test split apart")
plt.legend()
plt.tight_layout()
plt.savefig("train_vs_test_gap.png")
print("\nChart saved: train_vs_test_gap.png")
