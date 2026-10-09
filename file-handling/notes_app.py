# Day 19: file handling
# Type a few notes. Each line is written to notes.txt, then the
# file is read back and printed with line numbers. Run it twice:
# the second run overwrites the first, because the mode is "w".

print("Type your notes. Enter a blank line to stop.")

with open("notes.txt", "w") as f:
    while True:
        line = input("> ")
        if line == "":
            break
        f.write(line + "\n")

print("Your notes:")
with open("notes.txt") as f:
    number = 1
    for line in f:
        print(number, line.strip())
        number = number + 1
