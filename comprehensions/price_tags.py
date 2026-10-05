# price_tags.py
# Day 15 project: lambda + map.
# lambda p: p * 1.18 is a tiny one-expression function with
# no def needed. map runs it on every price and hands you
# a LAZY iterator, so wrap it in list() -- try printing
# map(...) without list() and you'll get a <map object>.
# Change the prices at the top and rerun.

prices = [100, 250, 80, 499]
with_tax = list(map(lambda p: round(p * 1.18, 2), prices))
print("Prices:       ", prices)
print("With 18% tax:", with_tax)
