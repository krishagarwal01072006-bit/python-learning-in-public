import pandas as pd

# run this from the pandas-1 folder, so read_csv finds scores.csv
df = pd.read_csv("scores.csv")

print(df["name"])
print(df[["name", "score"]])
print(df.iloc[0])
print(df.iloc[1:3])
