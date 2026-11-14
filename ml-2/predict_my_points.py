# Day 41, project 3: predict a player's points from three numbers.
# Run: python3 predict_my_points.py
# Type a player's minutes, field-goal attempts and FG% (as a
# decimal, e.g. 0.45), and the script predicts total points with
# the weights project 1 fitted on the 388 training players:
# -121.25 + (-0.039 x minutes) + (1.374 x attempts) + (249.52 x FG%).
# Minutes barely matters once attempts are known - that is the
# lesson of this post, not a bug in the weights.
intercept = -121.25
weight_minutes = -0.039
weight_attempts = 1.374
weight_fg_pct = 249.52

minutes = float(input("Minutes played in the season: "))
attempts = float(input("Field-goal attempts: "))
fg_pct = float(input("Field-goal % as a decimal (e.g. 0.45): "))

predicted = intercept + weight_minutes * minutes + weight_attempts * attempts + weight_fg_pct * fg_pct
print("Predicted total points:", round(predicted, 1))
print("Reality check: Anthony Davis, 2017 - 2708 minutes,")
print("1527 attempts, 0.504 FG% - scored 2099 points.")
print("This model would have guessed 1997.0. Day 39 guessed 1190.")
