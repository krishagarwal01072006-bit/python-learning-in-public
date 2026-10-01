# letter_counter.py
# Day 11 project: count how many times each character appears.
# Dict keys are characters, values are counts. .get(ch, 0)
# hands back 0 for characters we haven't seen yet, so we
# never trip over a missing key.
# Type anything and hit enter.

text = input("Type something: ")
counts = {}

for ch in text:
    counts[ch] = counts.get(ch, 0) + 1

print("Character counts:")
for ch in counts:
    print(ch, "appears", counts[ch], "time(s)")
