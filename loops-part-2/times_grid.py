# times_grid.py
# Day 7 project: the full times table, printed with nested loops.
# The outer loop walks the rows, the inner loop walks the columns.
# Change size, then rerun. Try 5, then try 12.

size = 10

for row in range(1, size + 1):
    for col in range(1, size + 1):
        print(row, "x", col, "=", row * col)
