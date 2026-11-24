# Day 51, project 1: meet the Delhi AQI data.
# Put city_day.csv (Kaggle: rohanrao/air-quality-data-in-india)
# in this same folder, then run: python3 delhi_aqi_explore.py
# Uses pandas (Days 33/35) and numpy (Days 29/31). One idea:
# before any model, look at what Delhi actually gives you.
# The target is AQI_Bucket, the 6 CPCB classes: Good,
# Satisfactory, Moderate, Poor, Very Poor, Severe.
# Day 25's bot REPORTED Delhi's AQI. This capstone PREDICTS it.
import pandas as pd
import numpy as np

df = pd.read_csv("city_day.csv")
print("All rows:", len(df), " Cities:", df["City"].nunique())

delhi = df[df["City"] == "Delhi"].copy()
print("Delhi rows:", len(delhi))
print("Date range:", delhi["Date"].min(), "to", delhi["Date"].max())

# Rows with no label cannot teach a classifier anything, so
# they go before the split. That is not cleaning, it is just
# dropping rows with no answer key.
delhi = delhi.dropna(subset=["AQI_Bucket"])
print("Delhi rows with a label:", len(delhi))

# Split BEFORE cleaning, Day 39's rule: any cleaning that
# learns from the whole file (like a median) would leak the
# test days into the training days.
train = delhi.sample(frac=0.8, random_state=7)
test = delhi.drop(train.index)
print("Train days:", len(train), " Test days:", len(test))

print("\nAQI_Bucket counts (all labelled Delhi days):")
print(delhi["AQI_Bucket"].value_counts().to_string())
print("\nDelhi mean AQI:", round(delhi["AQI"].mean(), 1))
print("Delhi median AQI:", round(delhi["AQI"].median(), 1))
print("Delhi AQI range:", int(delhi["AQI"].min()), "to", int(delhi["AQI"].max()))

# The dumb baseline: always guess the most common bucket.
common = delhi["AQI_Bucket"].value_counts().idxmax()
print("\nMost common bucket:", common)
print("Always-guess-it accuracy on ALL days:",
      round((delhi["AQI_Bucket"] == common).mean() * 100, 1), "%")
print("Always-guess-it accuracy on the TEST days:",
      round((test["AQI_Bucket"] == common).mean() * 100, 1), "%")

print("\nMissing values in the Delhi rows (%):")
print((delhi.isna().mean() * 100).round(1).to_string())
