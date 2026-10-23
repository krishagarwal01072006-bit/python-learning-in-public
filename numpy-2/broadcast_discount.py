import numpy as np

# prices at 2 stores for 3 products (rows = stores, cols = products)
grid = np.array([[100, 200, 300],
                 [150, 250, 350]])

# one discount per product. shape (3,) stretches across both rows.
discount = np.array([10, 20, 30])
print(grid - discount)

# gotcha: a (3,) row does NOT line up with a (3, 2) table
# np.array([10, 20, 30]) + np.array([[1, 2], [3, 4], [5, 6]])
# -> ValueError: operands could not be broadcast together with shapes (3,) (3,2)
# reshape it into a (3, 1) column and it stretches across the columns instead:
print(np.array([[10], [20], [30]]) + np.array([[1, 2], [3, 4], [5, 6]]))
