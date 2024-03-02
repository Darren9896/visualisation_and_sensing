import pandas as pd
import plotly.graph_objects as go

# Load the Excel file
data = pd.read_excel('Plastic_pollution_data.xlsx')

# Display the first few rows to understand its structure
continent_data = data.groupby('Continent')['Total Plastic Waste (Tonne)'].sum().reset_index()
continent_data['parent'] = ""  # Set the parent of continents as an empty string for the root level

# Prepare the country-level data
country_data = data[['country', 'Continent', 'Total Plastic Waste (Tonne)']].copy()
country_data.rename(columns={'country': 'name', 'Continent': 'parent', 'Total Plastic Waste (Tonne)': 'value'},
                    inplace=True)

# Combine continent and country data
hierarchy_data = pd.concat([
    continent_data.rename(columns={'Continent': 'name', 'Total Plastic Waste (Tonne)': 'value'}),
    country_data
], ignore_index=True)

# Create the circular packing chart
fig = go.Figure(go.Treemap(
    labels=hierarchy_data['name'],
    parents=hierarchy_data['parent'],
    values=hierarchy_data['value'],
    marker_colors=hierarchy_data['value'],
    branchvalues='total',
    textinfo="label+value"
))

fig.update_layout(margin=dict(t=10, l=0, r=0, b=10))

fig.show()
