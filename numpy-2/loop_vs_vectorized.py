import time

import numpy as np

# change me and rerun: try 100_000 or 10_000_000
n = 1_000_000

nums = list(range(n))
start = time.perf_counter()
total = 0
for x in nums:
    total += x
loop_time = time.perf_counter() - start

arr = np.arange(n)
start = time.perf_counter()
total_fast = arr.sum()
numpy_time = time.perf_counter() - start

print("loop  :", total, "->", round(loop_time, 3), "seconds")
print("numpy :", total_fast, "->", round(numpy_time, 4), "seconds")
