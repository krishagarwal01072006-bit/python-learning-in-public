import pandas as pd

# run this from the pandas-1 folder, so read_csv finds scores.csv
df = pd.read_csv("scores.csv")

print(df.head(3))
df.info()
print(df.describe())
