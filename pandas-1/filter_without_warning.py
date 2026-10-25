import pandas as pd

# run this from the pandas-1 folder, so read_csv finds scores.csv
df = pd.read_csv("scores.csv")

# editing a filtered slice warns you (SettingWithCopyWarning).
# Assign through .loc on the original frame instead:
df.loc[df["score"] > 85, "score"] = 100
print(df[df["score"] == 100])
