# Day 19: file handling
# Writes a small paragraph to sample.txt, then reads it back and
# counts lines and words with .split(). Edit the sample text and
# rerun to see the counts change.

sample = "machine learning needs data\ndata lives in files\nfiles are just text"

with open("sample.txt", "w") as f:
    f.write(sample)

lines = 0
words = 0
with open("sample.txt") as f:
    for line in f:
        lines = lines + 1
        words = words + len(line.split())

print("lines:", lines)
print("words:", words)
