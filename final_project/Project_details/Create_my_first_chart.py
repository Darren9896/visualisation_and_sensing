# Import libray
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# get the plastic pollution data files
read_plastic_pollution_dataset = pd.read_excel('Plastic_pollution_data.xlsx')


# This function here is to convert the tonne into a million metric tons
# Reference: I've lean how to convert the tonnes to a million in this website below
# https://matplotlib.org/stable/gallery/ticks/custom_ticker1.html#sphx-glr-gallery-ticks-custom-ticker1-py
def convert_tonne_into_million_metric_tons(y, pos):
    return f'{y / 1e6:.0f}M'


# Plotting size adjustment width and height
fig, ax = plt.subplots(figsize=(30, 10))

# this line of code is to sort dataset to make the chart more readable
data_sorted = read_plastic_pollution_dataset.sort_values(by='Total Plastic Waste (Tonne)', ascending=False)

# The number of the countries in my dataset ,In plastic pollution dataset,which has 202 row of dataset
Number_of_countries = 202
data_for_all_countries = data_sorted.head(Number_of_countries)

# Create the bar chart based on plastic pollution dataset
plastic_pollution_in_tons = range(len(data_for_all_countries))
bar_width = 0.8
ax.bar(plastic_pollution_in_tons, data_for_all_countries['Total Plastic Waste (Tonne)'], bar_width,
       label='Total Plastic Waste', color='orange')

ax.set_xlabel('Country')
ax.set_ylabel('Million Metric Tonne')
ax.set_title('Total Plastic Waste by Country in 2023')
# This line of code is to adjust each country names in each bar centre area
ax.set_xticks([i + bar_width / 20 for i in plastic_pollution_in_tons])
ax.set_xticklabels(data_for_all_countries['country'], rotation=90)
ax.legend()

# Apply the formatter to the y-axis and showing the result in a million metric tons
ax.yaxis.set_major_formatter(FuncFormatter(convert_tonne_into_million_metric_tons))

# Set the x-axis to start from the leftmost bar and add a little padding on the right in bar chart for clarity
ax.set_xlim(-0.5, len(data_for_all_countries) + 0.5)

# This line of codes here is to set the highers value in y-axis for 0 to 40 million metric tons
ax.set_ylim(0, 40e6)

# Showing the graph
plt.show()
