# model_deploy_check.py
# Day 3 project: if/elif/else decides whether our AI model ships.
# Feed it accuracy and latency — it answers: deploy, tune, or retrain.
# Press Enter to accept the defaults shown in [brackets].

def read_float(prompt, default):
    """Read a number; fall back to default on empty input or EOF."""
    try:
        raw = input(prompt).strip()
    except EOFError:
        print()  # keep the terminal tidy when stdin runs out
        return default
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"  '{raw}' is not a number — using default {default}.")
        return default

def check_model(accuracy, latency_ms):
    # The elif ladder: first True branch wins, the rest are skipped.
    if accuracy >= 95 and latency_ms <= 100:
        return "DEPLOY IT! High accuracy, fast enough. Ship it. 🚀"
    elif accuracy >= 90 and latency_ms <= 200:
        return "TUNABLE: decent model, but cut latency before launch. 🔧"
    elif accuracy >= 80:
        return "NEEDS WORK: retrain with more data, then re-check. 📊"
    else:
        return "RETRAIN: accuracy too low. Back to the training loop. 🛑"

accuracy = read_float("Model accuracy (0-100) [92]: ", 92.0)
latency = read_float("Latency in ms [150]: ", 150.0)

print(f"\nAccuracy: {accuracy}% | Latency: {latency} ms")
print(check_model(accuracy, latency))
print("Every classifier is just if/else at massive scale. 🤖")
