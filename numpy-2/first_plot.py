import matplotlib.pyplot as plt

# change me and rerun: edit these lists and watch the chart change
days = [1, 2, 3, 4, 5, 6, 7]
aqi = [151, 148, 142, 130, 135, 161, 194]

plt.plot(days, aqi)
plt.xlabel("day")
plt.ylabel("aqi")
plt.title("delhi aqi this week")
plt.show()  # without this line the figure never appears
