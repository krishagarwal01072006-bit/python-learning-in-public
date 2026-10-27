import pandas as pd

# run this from the pandas-2 folder, so read_csv finds messy.csv
df = pd.read_csv("messy.csv")

# fillna returns a new Series. This line alone changes nothing.
df["score"].fillna(0)
print("still missing:", df["score"].isna().sum())

# assign it back and the gaps are actually gone
df["score"] = df["score"].fillna(0)
print("still missing:", df["score"].isna().sum())
print(df)
