# login_attempts.py
# Day 7 project: a password gate with 3 attempts.
# A while loop counts your tries down. Get it right and break lets you in.
# Type a wrong password twice, then the right one: letmein

password = "letmein"
attempts_left = 3

while attempts_left > 0:
    guess = input("Enter password: ")
    if guess == "":
        print("Empty guess - that doesn't count. Try again.")
        continue
    if guess == password:
        print("Access granted. Welcome in.")
        break
    attempts_left = attempts_left - 1
    print("Wrong password.", attempts_left, "attempts left.")

if attempts_left == 0:
    print("Account locked. Call the front desk.")
