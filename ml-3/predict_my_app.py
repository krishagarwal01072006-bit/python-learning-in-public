# Day 43, project 3: predict whether YOUR app would be a hit.
# Run: python3 predict_my_app.py
# Type an app's reviews, installs, price, size and free/paid, and
# the script predicts hit (4.2 stars or more) or flop with the
# weights project 1 fitted on the 7,114 training apps:
# intercept 0.67, log_reviews 2.12, log_installs -1.65,
# Price -0.09, Size_MB -0.02, is_free -0.03, applied to
# standardised features (train means 8.27, 12.19, 0.84, 21.96,
# 0.93; train stds 3.85, 3.85, 14.72, 21.35, 0.25).
# Reviews and installs pull in opposite directions because they
# move together: once reviews are known, extra installs alone
# stop adding anything. That is the model splitting the credit
# between two numbers that tell almost the same story.
import numpy as np

weights = [0.67, 2.12, -1.65, -0.09, -0.02, -0.03]
means = [8.27, 12.19, 0.84, 21.96, 0.93]
stds = [3.85, 3.85, 14.72, 21.35, 0.25]

reviews = float(input("Reviews (e.g. 10000): "))
installs = float(input("Installs (e.g. 1000000): "))
price = float(input("Price in $ (0 if free): "))
size = float(input("Size in MB (e.g. 25): "))
free = input("Free app? (y/n): ").strip().lower()
is_free = 1 if free == "y" else 0

features = [np.log1p(reviews), np.log1p(installs), price, size, is_free]
score = weights[0]
for w, value, mu, sd in zip(weights[1:], features, means, stds):
    score += w * (value - mu) / sd
prob = 1 / (1 + np.exp(-score))
print(f"\nHit probability: {prob * 100:.1f}%")
if prob >= 0.5:
    print("Verdict: HIT (4.2 stars or more).")
else:
    print("Verdict: FLOP (under 4.2 stars).")

print("\nReality check from the test apps:")
print("Clash of Clans: 44,891,723 reviews, 100M installs, free,")
print("rated 4.6. This model gives it 95.6% - a hit, correctly.")
print("I'm Rich - Trump Edition: 275 reviews, 10,000 installs,")
print("$400 price, rated 3.6. This model gives it 13.9% - a flop,")
print("correctly. The $400 price tag did not help it.")
print("Las Vegas Lights FC: only 10 reviews, rated 4.9, but the")
print("model gives it 50.0% - a coin flip. Ten reviews tell it")
print("almost nothing, and the model says so.")
