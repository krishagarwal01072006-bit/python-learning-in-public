# grade_oracle.py
# Day 3 project: the classic elif ladder.
# Change score and rerun — Python stops at the FIRST true branch.

score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F — keep practicing")
