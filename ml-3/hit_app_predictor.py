# Day 43, project 1: classification - Hit App Predictor.
# Put the Kaggle file googleplaystore.csv (lava18/google-play-store-apps)
# in this same folder, then run: python3 hit_app_predictor.py
# Uses pandas (Days 33/35), numpy (Days 29/31) and the Day 39
# train/test split. One idea: a yes-or-no prediction instead of a
# number. Is a Play Store app highly rated (4.2 stars or more)?
# Logistic regression is linear regression's cousin: same weighted
# sum as Day 41, but a sigmoid squashes it into a probability,
# and 0.5 is the line between "hit" and "flop".
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("googleplaystore.csv")
df = df.drop_duplicates()
df = df.dropna(subset=["Rating"])
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

# The label: 1 means a hit (4.2 stars or more), 0 means a flop.
df["hit"] = (df["Rating"] >= 4.2).astype(int)
# Reviews and installs run into the millions, so take log1p first:
# log(1 + x) shrinks huge numbers down to a size the model can use.
df["log_reviews"] = np.log1p(df["Reviews"])
df["log_installs"] = np.log1p(df["Installs"])
df["is_free"] = (df["Type"] == "Free").astype(int)

# Same split as Days 39/41: 80% train, 20% test, random_state=7.
train = df.sample(frac=0.8, random_state=7)
test = df.drop(train.index)
print("Train apps:", len(train), " Test apps:", len(test))
print("Hits in the test apps:", round(test["hit"].mean() * 100, 1), "%")

features = ["log_reviews", "log_installs", "Price", "Size_MB", "is_free"]
# Standardise with the TRAIN mean and std only, so the test apps
# stay unseen. A feature ten million times bigger than the others
# would otherwise swallow the whole model.
mu = train[features].mean()
sd = train[features].std()

def make_x(data):
    return np.column_stack([np.ones(len(data))] + [((data[c] - mu[c]) / sd[c]).values for c in features])

train_x = make_x(train)
test_x = make_x(test)
train_y = train["hit"].values.astype(float)
test_y = test["hit"].values.astype(int)

# Sigmoid: squashes any weighted sum into a probability (0 to 1).
# np.clip stops the overflow I hit on the first run, when raw
# Reviews and Installs went straight in and numpy warned:
# RuntimeWarning: overflow encountered in exp
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

# Fit: gradient descent nudges the weights 2000 times so the
# predicted probabilities move towards the real 0s and 1s.
weights = np.zeros(train_x.shape[1])
for step in range(2000):
    prob = sigmoid(train_x @ weights)
    weights -= 0.1 * (train_x.T @ (prob - train_y)) / len(train_y)
print("Weights (intercept, log_reviews, log_installs, Price, Size_MB, is_free):", np.round(weights, 2))

def report(name, x, y):
    pred = (sigmoid(x @ weights) >= 0.5).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    acc = (tp + tn) / len(y)
    print(f"\n{name}: accuracy {acc * 100:.1f}%")
    print(f"Confusion matrix: TP {tp}  TN {tn}  FP {fp}  FN {fn}")
    print(f"Precision (of the apps called hits, how many really are): {tp / (tp + fp) * 100:.1f}%")
    print(f"Recall (of the real hits, how many were caught): {tp / (tp + fn) * 100:.1f}%")
    print(f"Flops spotted (of the real flops, how many were caught): {tn / (tn + fp) * 100:.1f}%")
    return tp, tn, fp, fn

report("Train", train_x, train_y)
tp, tn, fp, fn = report("Test", test_x, test_y)

# The dumb baseline: guess "hit" for every single app.
baseline = max(test_y.mean(), 1 - test_y.mean())
print(f"\nAlways-guess-hit accuracy on the test apps: {baseline * 100:.1f}%")

# Chart: the four confusion-matrix counts, so the trap is visible.
plt.bar(["Hits caught (TP)", "Flops caught (TN)", "Flops called hits (FP)", "Hits missed (FN)"], [tp, tn, fp, fn])
plt.title("Hit App Predictor: confusion matrix counts (test apps)")
plt.ylabel("Apps")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("hit_app_confusion.png")
print("\nChart saved: hit_app_confusion.png")
