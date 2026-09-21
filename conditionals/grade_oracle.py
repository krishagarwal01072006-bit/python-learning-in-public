# grade_oracle.py
# Day 3 project: the classic elif ladder.
# Turn a raw score into a letter grade — plus a fortune. 🔮

def ask(prompt):
    """Ask a question; return '' if stdin runs out (EOF)."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return ""

def grade(score):
    # Order matters: Python stops at the FIRST true branch.
    if score >= 90:
        return ("A", "Certified genius. The neural nets respect you.")
    elif score >= 80:
        return ("B", "Solid. One more training epoch and you're S-tier.")
    elif score >= 70:
        return ("C", "Average — like a model trained on 10 examples.")
    elif score >= 60:
        return ("D", "Barely passing. Time to debug your study habits.")
    else:
        return ("F", "Overfit to Netflix. Retrain and try again.")

raw = ask("Enter your score (0-100): ").strip()
if raw == "":
    print("No score entered. The oracle remains silent. 🔮")
else:
    try:
        score = float(raw)
    except ValueError:
        print(f"'{raw}' is not a number. The oracle is confused. 🔮")
    else:
        letter, fortune = grade(score)
        print(f"Score: {score:g} -> Grade: {letter}")
        print(f"🔮 {fortune}")
