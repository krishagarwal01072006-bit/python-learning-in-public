# aliasing_demo.py
# Day 9 project: the gotcha that got me — aliasing.
# b = a does NOT copy a list. Both names point at the same list,
# so editing through one changes the other. Watch it happen.
# Change the numbers at the top and rerun.

a = [1, 2, 3]
b = a   # not a copy! same list, two names

b.append(4)
print("a is:", a)
print("b is:", b)

b.pop()
print("After b.pop(), a is:", a)
