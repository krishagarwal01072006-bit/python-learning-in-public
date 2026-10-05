# square_maker.py
# Day 15 project: your first list comprehension.
# [x * x for x in range(n)] is a whole for-loop + append
# pattern squashed into one line. Read it right to left:
# for each x in range(n), make x * x, collect the results.
# Type a number when asked.

n = int(input("How many numbers: "))
squares = [x * x for x in range(n)]
print("Numbers:", list(range(n)))
print("Squares:", squares)
