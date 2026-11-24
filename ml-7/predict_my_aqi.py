# Day 51, project 3: predict MY AQI day.
# Run: python3 predict_my_aqi.py
# Type in today's 7 pollutant readings and the Day 51 model
# guesses the AQI bucket. The model is fitted on all 1,999
# labelled Delhi days here, after the train/test check in
# project 2 picked the approach. Same standardising as project 2.
# Try a clean winter morning: PM2.5 35, PM10 60, NO2 25,
# SO2 10, CO 1, O3 40, NH3 12. Then try a bad November day:
# PM2.5 380, PM10 550, NO2 90, SO2 25, CO 4, O3 20, NH3 45.
import pandas as pd
import numpy as np

df = pd.read_csv("city_day.csv")
delhi = df[df["City"] == "Delhi"].dropna(subset=["AQI_Bucket"])

features = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]
classes = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

mu = delhi[features].mean()
sd = delhi[features].std()

def make_x(data):
    filled = data[features].copy()
    for c in features:
        filled[c] = filled[c].fillna(mu[c])
    return np.column_stack([np.ones(len(data))] +
                           [((filled[c] - mu[c]) / sd[c]).values for c in features])

all_x = make_x(delhi)
all_y = np.array([classes.index(v) for v in delhi["AQI_Bucket"]])

def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

onehot = np.eye(6)[all_y]
weights = np.zeros((all_x.shape[1], 6))
for step in range(3000):
    prob = softmax(all_x @ weights)
    weights -= 0.1 * (all_x.T @ (prob - onehot)) / len(all_y)

print("Type in today's pollutant readings for Delhi.")
readings = []
for c in features:
    readings.append(float(input(f"{c}: ")))
row = np.array([[1] + [(readings[i] - mu[features[i]]) / sd[features[i]]
                       for i in range(len(features))]])
probs = softmax(row @ weights)[0]
order = probs.argsort()[::-1]
print(f"\nPredicted bucket: {classes[order[0]]} ({probs[order[0]] * 100:.1f}%)")
print("Top 3 guesses:")
for i in order[:3]:
    print(f"  {classes[i]}: {probs[i] * 100:.1f}%")
print("\nIf it says Good, check twice: Delhi only had 21 Good days")
print("in 5.5 years, and this model has never predicted one.")
