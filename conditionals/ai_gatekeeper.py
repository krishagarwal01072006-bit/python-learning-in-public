# ai_gatekeeper.py
# Day 3 project: the gatekeeper decides if you're a robot.
# A playful quiz built on == comparisons and and/or logic.
# (Remember: == compares, = assigns. `if q1 = "19":` is a SyntaxError!)

def ask(prompt):
    """Ask a question; return '' if stdin runs out (EOF)."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return ""

print("🤖 AI GATEKEEPER: prove you're human.")
print("Answer 3 questions. Score 2+ to pass.\n")

score = 0

# == compares two strings for equality.
q1 = ask("1) What is 9 + 10? ").strip()
if q1 == "19":
    print("  Correct!")
    score += 1
else:
    print("  The gatekeeper raises an eyebrow...")

# or accepts several right answers.
q2 = ask("2) Do you dream? (yes/no) ").strip().lower()
if q2 == "yes" or q2 == "yeah" or q2 == "y":
    print("  Suspiciously poetic. Correct!")
    score += 1
else:
    print("  A robot would say no...")

# and needs EVERY part to be true.
q3 = ask("3) Type the word 'human' twice, separated by a space: ")
words = q3.strip().lower().split()
if len(words) == 2 and words[0] == "human" and words[1] == "human":
    print("  Nailed it!")
    score += 1
else:
    print("  The gatekeeper is unimpressed.")

print(f"\nFinal score: {score}/3")
if score >= 2:
    print("✅ VERIFIED: probably human. Welcome!")
else:
    print("❌ DENIED: the robots are suspicious of you.")
