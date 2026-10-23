import numpy as np

# 7 days of high temps for 3 cities (rows = cities, cols = days)
temps = np.array([
    [31, 32, 30, 29, 31, 33, 32],  # delhi
    [28, 28, 29, 27, 28, 29, 30],  # mumbai
    [24, 25, 24, 23, 25, 26, 25],  # bengaluru
])

# axis=1 means "along each row", so this gives one mean per city
print("mean per city:", temps.mean(axis=1))
print("hottest reading overall:", temps.max())
print("sum of every reading:", temps.sum())
