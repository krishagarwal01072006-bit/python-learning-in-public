# typing_tour.py
# Day 1 project: one variable, many types.
# Python lets the same box hold anything — watch it change.

value = 42
print(value)
print(type(value))

value = "hello ai"   # same variable, brand-new type. Python doesn't mind.
print(value)
print(type(value))

value = 3.5
print(value)
print(type(value))

print("--- gotcha 1: / vs // ---")
print(7 / 2)    # true division, always a float: 3.5
print(7 // 2)   # floor division, rounds down: 3

print("--- gotcha 2: precedence ---")
print(2 + 3 * 4)      # * runs first: 14
print((2 + 3) * 4)    # brackets win: 20
