# grade_calculator.py
# Day 13 project: a function that takes a list and returns
# a result. average() loops over the marks, totals them,
# and RETURNS the average so the caller can print it or
# reuse it. Change the marks at the top and rerun.

def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / len(marks)

ria = [88, 74, 91]
dev = [65, 91, 78]

ria_avg = average(ria)
dev_avg = average(dev)
print("Ria average:", ria_avg)
print("Dev average:", dev_avg)
print("Class average:", (ria_avg + dev_avg) / 2)
