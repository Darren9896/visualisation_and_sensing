# using pandas library as pd to read my xlsx files
import pandas as pd

# get plastic pollution dataset excel file
read_plastic_pollution_dataset = pd.read_excel('Plastic_pollution_data.xlsx')

# Print out the dataset result to check if any data are missing
print(read_plastic_pollution_dataset)
