# score_tracker.py
# Day 9 project: collect test scores, then report them sorted.
# append() grows the list, sort() orders it, len() counts it.
# Type the number of scores first, then each score.

count = int(input("How many scores? "))
scores = []

for n in range(count):
    s = int(input("Enter score: "))
    scores.append(s)

scores.sort()
print("Sorted scores:", scores)
print("You entered", len(scores), "scores.")
print("Top score:", scores[len(scores) - 1])
