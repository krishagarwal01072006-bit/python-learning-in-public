# word_lengths.py
# Day 15 project: dict comprehensions.
# {n: len(n) for n in names} builds a whole dictionary in
# one line: each name becomes a key, its length the value.
# Same idea as a list comprehension, but with key: value
# pairs. Change the names at the top and rerun.

names = ["aria", "devansh", "zo", "krish"]
lengths = {n: len(n) for n in names}
print("Names:  ", names)
print("Lengths:", lengths)
