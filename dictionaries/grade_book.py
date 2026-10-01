# grade_book.py
# Day 11 project: nested dictionaries.
# Outer keys are students, values are dicts of subject -> marks.
# Loop over the outer dict, then loop the inner dict, and
# print each student's average.
# Change the marks at the top and rerun.

grades = {
    "ria": {"math": 88, "english": 74},
    "dev": {"math": 65, "english": 91},
    "ana": {"math": 95, "english": 87},
}

for student in grades:
    marks = grades[student]   # the inner dict for this student
    total = 0
    for subject in marks:
        total = total + marks[subject]
    average = total / len(marks)
    print(student, "average:", average)
