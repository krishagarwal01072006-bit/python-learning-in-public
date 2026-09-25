# multiplication_table.py
# Day 5 project: the times table of any number you pick.
# Type a number and press Enter. Try 7, then try 12.

number = int(input("Which times table? "))

for i in range(1, 11):
    print(number, "x", i, "=", number * i)
