import numpy as np

# shape and dtype: the two questions to ask any array
grid = np.arange(12).reshape(3, 4)

print("shape:", grid.shape)   # (rows, columns)
print("dtype:", grid.dtype)   # every element is the same type
print(grid)
print("rows:", grid.shape[0], "| cols:", grid.shape[1])

flat = grid.reshape(12)       # same data, new shape
print("flattened:", flat)
