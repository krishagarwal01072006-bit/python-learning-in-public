# ai_training_cost.py
# Day 1 project: variables + operators in action.
# Estimates what a hypothetical AI training run would cost.
# Change the numbers below and rerun — variables are yours to play with.

# --- Inputs (edit me!) ---
gpus = 8                  # number of GPUs in the cluster
gpu_cost_per_hour = 2.50  # rental price per GPU, in dollars
training_hours = 72       # how long training runs, in hours
power_per_gpu_hour = 0.08  # extra electricity cost per GPU-hour

# --- Operators do the heavy lifting ---
gpu_hours = gpus * training_hours            # multiplication
rental_cost = gpu_hours * gpu_cost_per_hour  # multiplication again
power_cost = gpu_hours * power_per_gpu_hour  # and again
total_cost = rental_cost + power_cost        # precedence: * ran before +
avg_per_hour = total_cost / training_hours   # / gives a float
full_days = training_hours // 24             # // floors: whole days only

# --- Output ---
print(f"Training on {gpus} GPUs for {training_hours} hours ({full_days} days):")
print(f"  GPU-hours used: {gpu_hours}")
print(f"  Rental cost:    ${rental_cost:,.2f}")
print(f"  Power cost:     ${power_cost:,.2f}")
print(f"  TOTAL:          ${total_cost:,.2f}")
print(f"  Avg per hour:   ${avg_per_hour:,.2f}")
print("A neural net is just millions of variables in named boxes —")
print("and every one of them costs money to update. 💸")
