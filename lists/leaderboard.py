# leaderboard.py
# Day 9 project: sort a list of scores and read the podium.
# sort() orders smallest first, so the winners live at the END.
# The last valid index is len(scores) - 1 (IndexError lesson!).
# Change the scores at the top and rerun to crown a new winner.

scores = [87, 64, 95, 72, 58, 91]

scores.sort()
print("Scores, low to high:", scores)
print("Winner:", scores[len(scores) - 1])
print("Runner-up:", scores[len(scores) - 2])
print("Third place:", scores[len(scores) - 3])
print("Players:", len(scores))
