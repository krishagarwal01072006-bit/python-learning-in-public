# countdown.py
# Day 5 project: a launch countdown, built with range() stepping backwards.
# Change start, then rerun.

start = 10

for second in range(start, 0, -1):
    print(second, "...")

print("LIFTOFF!")
print("The -1 step is what makes range() walk backwards.")
