# Day 17: exceptions
# Ask the user for their age. If they type letters instead of
# digits, int() raises a ValueError and the program explains
# instead of crashing.

try:
    age = int(input("Your age: "))
    print("Next year you will be", age + 1)
except ValueError:
    print("Not a number. Try again with digits only.")
