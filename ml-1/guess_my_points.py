# Day 39, project 3: guess a player's points from minutes alone.
# Run: python3 guess_my_points.py
# Type a minutes total, and the script predicts total points
# with the rule project 1 fitted: 0.4393 points per minute,
# learned from the 389 training players. Minutes alone cannot
# see talent, so stars will beat this guess by a lot.
ratio = 0.4393

minutes = float(input("Minutes played in the season: "))
predicted = ratio * minutes
print("Predicted total points:", round(predicted, 1))
print("Reality check: Anthony Davis played 2708 minutes in 2017")
print("and scored 2099 points. This rule would have guessed 1190.")
