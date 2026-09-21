# typing_tour.py
# Day 1 project: Python variables change type on the fly.
# Watch the gotchas live: // vs / and operator precedence.

value = 42
print(f"value = {value!r:>12}, type = {type(value).__name__}")

value = "hello, ai"  # same box, brand-new type — Python doesn't mind!
print(f"value = {value!r:>12}, type = {type(value).__name__}")

value = 3.5
print(f"value = {value!r:>12}, type = {type(value).__name__}")

print()
print("Gotcha 1 — / vs // :")
print(f"  7 / 2  = {7 / 2}   (true division, always a float)")
print(f"  7 // 2 = {7 // 2}     (floor division, rounds down)")

print()
print("Gotcha 2 — precedence (* and ** beat +):")
print(f"  2 + 3 * 4   = {2 + 3 * 4}")
print(f"  (2 + 3) * 4 = {(2 + 3) * 4}   (parentheses win)")

print()
print("Gotcha 3 — mixing types bites:")
try:
    result = "5" + 5
except TypeError as err:
    print(f'  "5" + 5 -> TypeError: {err}')
    print("  Fix it: int('5') + 5 =", int("5") + 5)
