# Day 51, project 2: the AQI category predictor.
# Put city_day.csv (Kaggle: rohanrao/air-quality-data-in-india)
# in this same folder, then run: python3 aqi_category_predictor.py
# Uses pandas (Days 33/35), numpy (Days 29/31) and the Day 43
# logistic regression, grown up: Day 43 predicted yes-or-no
# with one sigmoid. Six buckets need six scores, so this is
# softmax regression: one weighted sum per bucket, then the
# scores are turned into six probabilities that add up to 1.
# Features: the 7 pollutants. Xylene is dropped on purpose:
# 38.6% of Delhi's Xylene readings are missing, and Day 47
# taught me what a gappy feature does to a model.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("city_day.csv")
delhi = df[df["City"] == "Delhi"].dropna(subset=["AQI_Bucket"])

# Split BEFORE cleaning, Day 39's rule.
train = delhi.sample(frac=0.8, random_state=7)
test = delhi.drop(train.index)
print("Train days:", len(train), " Test days:", len(test))

features = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]
classes = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

# Median-fill and standardise with TRAIN numbers only, so the
# test days stay unseen. My first run skipped this step and fed
# the raw readings straight in: PM2.5 runs up to 1000 while CO
# barely reaches 10, the weights ballooned to 86.8, and the
# test accuracy was 44.5%. Same model, same data, standardised:
# 73.5%. Scale is not a detail, it is the whole game.
mu = train[features].mean()
sd = train[features].std()

def make_x(data):
    filled = data[features].copy()
    for c in features:
        filled[c] = filled[c].fillna(mu[c])
    return np.column_stack([np.ones(len(data))] +
                           [((filled[c] - mu[c]) / sd[c]).values for c in features])

train_x = make_x(train)
test_x = make_x(test)
train_y = np.array([classes.index(v) for v in train["AQI_Bucket"]])
test_y = np.array([classes.index(v) for v in test["AQI_Bucket"]])

# Softmax: the multi-class sigmoid. Subtract the row max first
# so exp() never overflows, the Day 43 lesson.
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

# One-hot targets: each day is a 1 in its own bucket, 0 elsewhere.
train_onehot = np.eye(6)[train_y]

# Fit: gradient descent nudges the 6 x 8 weight table 3000 times.
weights = np.zeros((train_x.shape[1], 6))
for step in range(3000):
    prob = softmax(train_x @ weights)
    weights -= 0.1 * (train_x.T @ (prob - train_onehot)) / len(train_y)
print("Biggest weight after standardising:", round(float(np.abs(weights).max()), 2))

def report(name, x, y):
    pred = softmax(x @ weights).argmax(axis=1)
    acc = (pred == y).mean() * 100
    print(f"\n{name}: accuracy {acc:.1f}%")
    print("Recall per bucket (of the real days in each bucket, how many were caught):")
    recalls = []
    for i, c in enumerate(classes):
        days = (y == i).sum()
        recall = (pred[y == i] == i).mean() * 100 if days else 0
        recalls.append(recall)
        print(f"  {c}: {days} days, recall {recall:.1f}%")
    return acc, recalls

train_acc, _ = report("Train", train_x, train_y)
test_acc, recalls = report("Test", test_x, test_y)

# The dumb baseline: always guess Poor, the most common bucket.
baseline = (test_y == classes.index("Poor")).mean() * 100
print(f"\nAlways-guess-Poor accuracy on the test days: {baseline:.1f}%")
print(f"The model beats the dumb baseline by {test_acc - baseline:.1f} points.")

# Chart: recall per bucket, so the clean end is visible.
plt.bar(classes, recalls)
plt.title("AQI Predictor: recall per bucket (test days)")
plt.ylabel("Recall (%)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("aqi_recall.png")
print("\nChart saved: aqi_recall.png")
