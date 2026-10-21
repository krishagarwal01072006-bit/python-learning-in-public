import numpy as np

# Why arrays exist: math on the WHOLE thing at once
celsius = [31, 29, 33, 28, 30]

# Python list: loop it yourself
fahrenheit_list = [(c * 9 / 5) + 32 for c in celsius]

# numpy array: the operation applies to every element
fahrenheit_arr = (np.array(celsius) * 9 / 5) + 32

print("list version:", fahrenheit_list)
print("array version:", fahrenheit_arr)
print("average temp:", np.array(celsius).mean())
