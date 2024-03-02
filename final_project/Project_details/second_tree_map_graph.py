# Import libray
# https://plotly.com/python/treemaps/
import pandas as pd
import plotly.express as px

# To get the data from plastic pollution data excel file
read_plastic_pollution_dataset = pd.read_excel('Plastic_pollution_data.xlsx')

# Sort data only review the Continent and country
sort_data = read_plastic_pollution_dataset.groupby(['Continent', 'country'], as_index=False)[('Total Plastic '
                                                                                                    'Waste ('
                                                                                                    'Tonne)')].sum()
# This line of code is to create the tree map, the values is each country total plastic waste data
# The color will follow by the plastic waste amount from higher amount of red, medium: yellow, low:green in graphs
fig = px.treemap(sort_data,
                 path=['Continent', 'country'],  # create the tree map follow by continent and to country
                 values='Total Plastic Waste (Tonne)',  # box size will follow by amount of Plastic waste in each
                 # country
                 title='Total Plastic Waste by Country in 2023',  # This is my tree map titles
                 color='Total Plastic Waste (Tonne)',  # Color the treemap by plastic waste
                 color_continuous_scale='RdYlGn_r',  # Color scale from Red > Yellow > green
                 )

# This line of code will display the result in tree map format
fig.show()