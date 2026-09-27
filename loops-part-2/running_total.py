# running_total.py
# Day 7 project: keep a running total until you type 0.
# Type a number and press Enter each time. 0 means "I am done adding".
# Try 5, then 10, then 3, then 0.

total = 0

while True:
    number = int(input("Add a number (0 to stop): "))
    if number == 0:
        break
    total = total + number
    print("Running total:", total)

print("Final total:", total)
