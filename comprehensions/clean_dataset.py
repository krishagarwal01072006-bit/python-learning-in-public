# clean_dataset.py
# Day 15 project: a comprehension with an if filter.
# These are raw readings from a sensor. The negative ones
# are glitches (junk data), so [r for r in readings if
# r >= 0] keeps only the good ones. One line, same as the
# cleaning step data people run before feeding numbers
# into a model. Change the readings at the top and rerun.

readings = [12, -3, 45, -1, 30, 51, -9, 27]
good = [r for r in readings if r >= 0]
print("Raw:  ", readings)
print("Clean:", good)
print("Dropped", len(readings) - len(good), "bad readings")
