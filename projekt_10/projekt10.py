import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

data = pd.read_csv("owid-covid-data.txt", sep=",")

data_poland = data[data.location == "Poland"]

data_poland["moving_average"] = data_poland["new_cases"].rolling(window=14).mean()


dates = data_poland["date"]
locator = mticker.MultipleLocator(200)
fig, ax = plt.subplots()
ax.bar(x=dates, height=data_poland["new_cases"], label="New cases")
ax.plot(dates, data_poland["moving_average"], color="red", label="Moving average")
ax.xaxis.set_major_locator(locator)
ax.set_xlabel("Date")
ax.set_title("New cases (Poland)")
plt.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(dates, data_poland["new_cases"]/data_poland["new_tests"])
ax.set_xlabel("Date")
ax.set_title("New cases per new tests (Poland)")
ax.xaxis.set_major_locator(locator)
plt.legend()
plt.show()