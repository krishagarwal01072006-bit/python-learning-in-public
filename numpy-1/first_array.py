import numpy as np

# Four ways to make your first array
temps = np.array([31, 29, 33, 28, 30])      # from a Python list
count = np.arange(5)                         # 0..4, like range()
empty = np.zeros(3)                          # placeholder of zeros
ones = np.ones((2, 2))                       # 2x2 block of ones

print(temps, "-> shape:", temps.shape, "| type:", temps.dtype)
print(count)
print(empty)
print(ones)
