import pandas as pd

# run this from the pandas-1 folder, so read_csv finds scores.csv
df = pd.read_csv("scores.csv", index_col="name")

# loc uses labels, iloc uses positions. Mixing them up is the trap.
print(df.loc["Asha"])
print(df.iloc[0])

try:
    print(df.loc[0])
except KeyError:
    print("KeyError: 0 - loc wants the label 'Asha', not position 0")
