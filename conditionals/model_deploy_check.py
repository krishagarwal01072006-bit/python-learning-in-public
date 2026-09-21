# model_deploy_check.py
# Day 3 project: if/elif/else decides whether our AI model ships.
# Try changing accuracy and latency, then rerun.

accuracy = 97   # model accuracy, out of 100
latency = 80    # response time in milliseconds

if accuracy >= 95 and latency <= 100:
    print("DEPLOY IT! High accuracy and fast enough.")
elif accuracy >= 90:
    print("TUNABLE: decent model, needs work before launch.")
else:
    print("RETRAIN: back to the training data.")

print("Every classifier is just if/else at massive scale.")
