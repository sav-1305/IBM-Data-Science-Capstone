#-IMPORTS---------------------------------------------------------#
import pandas as pd 
import numpy as np 
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

#-READ-DATAFRAME--------------------------------------------------#
spacexdf    = pd.read_csv(r"C:\Users\HP\Downloads\CSV Files\spacex_launch_dash.csv")
max_payload = spacexdf['Payload Mass (kg)'].max()
min_payload = spacexdf['Payload Mass (kg)'].min()

#-CREATE-DASH-APPLICATION-----------------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])

#-CREATE-APP-LAYOUT-----------------------------------------------#
app.layout = html.Div(children=[
    
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center', 
                'color': '#503D36',
            'font-size': 40
        },
    ),

    # TASK 1: ADD A DROPDOWN
    html.P("LAUNCH SITE:", style={'text-align':'center'}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'ALL Sites',      'value': 'ALL'},
            {'label': 'CCAFS LC-40',    'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E',    'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A',     'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40',   'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder='Select A Launch Site here',
        searchable=True
    ),

    html.Br(),

    # # TASK 2: ADD A PIE CHART
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: ADD A SLIDER
    html.P("PAYLOAD RANGE(KG):", style={'text-align':'center'}),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=500,
        marks={
            0: '0',
            10000: '10000'
        },
        value=(min_payload, max_payload)
    ),

    # TASK 4: ADD A SCATTER PLOT
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

#-CALLBACK-FUNCTIONS-------------------------------------------#
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacexdf[spacexdf['Launch Site'] == entered_site]
    
    if entered_site == 'ALL':
        fig = px.pie(
            spacexdf,
            values='class',
            names='Launch Site',
            title='Success Rate of All Launch Sites'
        )
        return fig
    else:
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(
            names=success_counts.index,
            values=success_counts.values,
            title=f'Success Rate of {entered_site}'
        )
        return fig
    
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacexdf[spacexdf['Launch Site'] == entered_site]

    if entered_site == 'ALL':
        fig = px.scatter(
            spacexdf,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Success Rate of Sites with Payload Mass Range {payload_range[0]} to {payload_range[1]} (kg)'
        )
    else:
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Success Rate of {entered_site} with varying Payload Mass (kg)'
        )
    fig.update_layout(
        xaxis=dict(range=[payload_range[0], payload_range[1]])
    )
    return fig

#-RUN-THE-APP--------------------------------------------------#
if __name__ == '__main__':
    app.run_server(debug=True)