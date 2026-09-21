# ai_training_cost.py
# Day 1 project: variables + operators.
# Change the numbers below and rerun — the cost updates itself.

gpus = 8               # how many GPUs we rent
price_per_hour = 2.5   # dollars per GPU per hour
hours = 72             # how long training runs

total_gpu_hours = gpus * hours
total_cost = total_gpu_hours * price_per_hour
days = hours // 24     # // is floor division: whole days only

print("GPUs:", gpus)
print("Total GPU-hours:", total_gpu_hours)
print("Training days:", days)
print("Total cost: $", total_cost)
print("A neural net is millions of variables — and each one costs money to train.")
