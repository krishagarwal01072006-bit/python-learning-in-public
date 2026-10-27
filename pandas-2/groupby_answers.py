import pandas as pd

# run this from the pandas-2 folder, so read_csv finds messy.csv
df = pd.read_csv("messy.csv")
df = df.drop_duplicates().dropna()

# one line per question: mean score per subject, plus how many rows each had
print(df.groupby("subject")["score"].mean())
print(df.groupby("subject")["score"].agg(["mean", "count"]))
