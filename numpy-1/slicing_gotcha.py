import numpy as np

# Slicing looks like lists. It is not.
scores = np.array([10, 20, 30, 40, 50])

first_three = scores[:3]   # a slice of the array
first_three[0] = 999       # change the slice...

print("slice:", first_three)
print("original:", scores)  # ...and the original changed too!

# A slice is a VIEW into the same memory, not a copy.
# Want an independent copy? Ask for one:
safe = scores[:3].copy()
safe[0] = -1
print("copy:", safe)
print("original untouched:", scores)
