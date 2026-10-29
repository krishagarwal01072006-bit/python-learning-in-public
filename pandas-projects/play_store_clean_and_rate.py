# Day 37, project 1: Google Play Store cleaning + ratings analysis.
# Put the Kaggle file googleplaystore.csv (lava18/google-play-store-apps)
# in this same folder, then run: python3 play_store_clean_and_rate.py
# Uses only pandas taught on Days 33 and 35: read_csv, drop_duplicates,
# dropna, groupby + agg, sort_values, value_counts, df.plot().
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("googleplaystore.csv")
print("Rows at the start:", len(df))

df = df.drop_duplicates()
df = df.dropna(subset=["Rating"])
print("Rows after dropping duplicates and unrated apps:", len(df))

# Cleaning, one dirty column at a time.
# Installs looks like "1,000,000+": strip the + and commas, then to numbers.
# One corrupt row has the word "Free" sitting in Installs (and "Everyone"
# in Price), which crashed the first run with:
# ValueError: Unable to parse string "Free" at position 8644
# errors="coerce" turns those into NaN instead of crashing.
df["Installs"] = df["Installs"].str.replace("+", "", regex=False)
df["Installs"] = df["Installs"].str.replace(",", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")
# Price looks like "$2.99": strip the $ sign, then to numbers.
df["Price"] = df["Price"].str.replace("$", "", regex=False)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
# Size looks like "19M": strip the M, then to numbers.
# "Varies with device" and "19k" cannot convert, so they become NaN.
df["Size_MB"] = pd.to_numeric(df["Size"].str.replace("M", "", regex=False), errors="coerce")

# Those coerced NaNs mark the corrupt row, so drop it before asking questions.
df = df.dropna(subset=["Installs", "Price"])

# Krish's own questions, not a tutorial's:
# 1. Which category has the most apps?
print("\nTop 5 categories by app count:")
print(df["Category"].value_counts().head(5))

# 2. Which category rates highest, counting only categories with
# at least 100 rated apps, so one 5-star app cannot win it alone?
by_category = df.groupby("Category")["Rating"].agg(["mean", "count"])
by_category = by_category[by_category["count"] >= 100]
print("\nHighest-rated categories (100+ rated apps):")
print(by_category.sort_values("mean", ascending=False).head(5))

# 3. Do free apps rate differently from paid apps, and do they install more?
print("\nFree vs paid:")
print(df.groupby("Type").agg(mean_rating=("Rating", "mean"), mean_installs=("Installs", "mean")))

# 4. Chart it, with the one-line plot from Day 35.
df["Category"].value_counts().head(5).plot(kind="bar")
plt.title("Top 5 Play Store categories by app count")
plt.ylabel("Apps")
plt.savefig("play_store_top_categories.png")
print("\nChart saved: play_store_top_categories.png")
