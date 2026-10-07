# Day 17: exceptions
# Try to open a dataset file. Run this as-is: dataset.csv does not
# exist yet, so the FileNotFoundError path runs. Then create an
# empty dataset.csv next to this script and rerun to see the
# else path.

try:
    f = open("dataset.csv")
except FileNotFoundError:
    print("dataset.csv is missing. Download the dataset first.")
else:
    lines = 0
    for line in f:
        lines = lines + 1
    f.close()
    print("File opened. It has", lines, "lines.")
finally:
    print("Open attempt finished.")
