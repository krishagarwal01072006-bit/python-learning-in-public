# add_calculator.py
# Day 13 project: return vs print.
# add() RETURNS the sum instead of printing it, so the
# caller can use the result in more math. A version that
# only print()ed would hand back None and break the line
# that adds the tip.
# Type two numbers when asked.

def add(a, b):
    return a + b

x = int(input("First number: "))
y = int(input("Second number: "))
total = add(x, y)
print("Total:", total)
print("Total + 10:", total + 10)
