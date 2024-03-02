# https://www.csc2.ncsu.edu/faculty/healey/msa/dash/
# Import libary
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

#This line of code get the data from my Plastic Pollution excel files
Total_Plastic_Waste_Data = pd.read_excel('Plastic_pollution_data.xlsx')

# https://dash.plotly.com/layout
# The initialized layout to setup the dash
app = dash.Dash(__name__)

app.layout = html.Div([
    # THis w
    dcc.Graph(id='plastic-waste-treemap', style={'height': '90vh', 'width': '100%'}),
    html.Div([
        html.Label('Filter from 0 to 10,000 tonne:'),
        dcc.RangeSlider(
            id='small-range-slider',
            min=0,
            max=1e4,
            step=100,
            marks={i: '{}Kt'.format(int(i/1e3)) for i in range(0, int(1e4)+1, 2000)},
            value=[0, 1e4]
        ),
    ]),
    html.Div([
        html.Label('Filter from 10K tonnes to 1M tonnes:'),
        dcc.RangeSlider(
            id='medium-range-slider',
            min=1e4,
            max=1e6,
            step=1e4,
            marks={
                1e4: '10Kt',
                **{i: '{}Kt'.format(int(i / 1e3)) for i in range(int(1e5), int(1e6), int(1e5))},

                1e6: '1M',
            },
            value=[1e4, 1e6]
        ),
    ]),
    html.Div([
        html.Label('Filter from 1M Tonnes to 40M Tonnes:'),
        dcc.RangeSlider(
            id='large-range-slider',
            min=1e6,
            max=40e6,
            step=1e6,
            marks={
                1e6: '1M Tonnes',
                **{i: '{}M'.format(int(i / 1e6)) for i in range(int(0), int(40e6), int(5e6))},
                40e6: '40M Tonnes',
            },
            value=[1e6, 40e6]
        ),
    ]),
])

# https://plotly.com/python/setting-graph-size/
@app.callback(
    Output('plastic-waste-treemap', 'figure'),
    [Input('small-range-slider', 'value'),
     Input('medium-range-slider', 'value'),
     Input('large-range-slider', 'value')]
)
def update_figure(small_range, medium_range, large_range):

    filtered_data = pd.DataFrame()

    if small_range:
        filtered_data = pd.concat(
            [filtered_data, Total_Plastic_Waste_Data[Total_Plastic_Waste_Data['Total Plastic Waste (Tonne)'].between(small_range[0], small_range[1])]])
    if medium_range:
        filtered_data = pd.concat(
            [filtered_data, Total_Plastic_Waste_Data[Total_Plastic_Waste_Data['Total Plastic Waste (Tonne)'].between(medium_range[0], medium_range[1])]])
    if large_range:
        filtered_data = pd.concat(
            [filtered_data, Total_Plastic_Waste_Data[Total_Plastic_Waste_Data['Total Plastic Waste (Tonne)'].between(large_range[0], large_range[1])]])

    filtered_data = filtered_data.drop_duplicates()

    continent_data = filtered_data.groupby('Continent')['Total Plastic Waste (Tonne)'].sum().reset_index()
    continent_data['parent'] = ""

    country_data = filtered_data[['country', 'Continent', 'Total Plastic Waste (Tonne)']].copy()
    country_data.rename(columns={'country': 'name', 'Continent': 'parent', 'Total Plastic Waste (Tonne)': 'value'},
                        inplace=True)

    hierarchy_data = pd.concat(
        [continent_data.rename(columns={'Continent': 'name', 'Total Plastic Waste (Tonne)': 'value'}), country_data],
        ignore_index=True)

    fig = go.Figure(go.Treemap(
        labels=hierarchy_data['name'],
        parents=hierarchy_data['parent'],
        values=hierarchy_data['value'],
        textposition='middle center',
        hovertemplate="<b>%{label}</b><br>%{value} Tonnes<extra></extra>",
        texttemplate="<b>%{label}</b><br>%{value} Tonnes",
        textfont=dict(
            size=20,
            color='white'
        ),
        marker=dict(
            colors=hierarchy_data['value'],
            colorscale=[
                # https://www.heavy.ai/blog/12-color-palettes-for-telling-better-stories-with-your-data
                [0.0, 'rgb(113, 113, 133)'],
                [0.02, 'rgb(7, 84, 183)'],
                [0.04, 'rgb(109, 75, 75)'],
                [0.06, 'rgb(80, 63, 63)'],
                [0.095, 'rgb(107, 80, 10)'],
                [0.1, 'rgb(247, 132, 41)'],
                [0.25, 'rgb(178, 224, 97)'],
                [0.5, 'rgb(105, 41, 196)'],
                [0.75, 'rgb(253, 204, 229)'],
                [1.0, 'rgb(87, 4, 8)'],
            ],
            colorbar=dict(title='Total Plastic Waste<br>(Tonne)'),
        ),
        branchvalues='total',
        textinfo="label+value"
    ))

    fig.update_layout(
        title={
            'text': "Global Plastic Waste in 2023",
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },

        margin=dict(t=65, l=0, r=0, b=0))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)