import pandas as pd

# run this from the pandas-2 folder, so read_csv finds messy.csv
df = pd.read_csv("messy.csv")
print("before:", df.shape)
print(df)

# one exact duplicate row, and two missing scores
df = df.drop_duplicates()
print("after drop_duplicates:", df.shape)

# dropna throws away rows with a gap; fillna keeps them with a default
print(df.dropna())
