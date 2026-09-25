# fizzbuzz.py
# Day 5 project: the classic interview question, built with a loop + if.
# % gives the remainder after division. 6 % 3 is 0, so 6 is divisible by 3.

for n in range(1, 21):
    if n % 3 == 0 and n % 5 == 0:
        print("fizzbuzz")
    elif n % 3 == 0:
        print("fizz")
    elif n % 5 == 0:
        print("buzz")
    else:
        print(n)
