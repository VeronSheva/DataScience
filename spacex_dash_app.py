# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                            
                                dcc.Dropdown(id='site-dropdown',  value='ALL', searchable=True,
                                placeholder='Select a Launch Site here',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}]),
                                html.Br(), 

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'}, value=[min_payload, max_payload]),
                                
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    data = spacex_df.groupby(['Launch Site'])['class'].count()
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        # names='Launch Site', 
        title='Launch success count for all sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['class'])['Launch Site'].count()

        fig = px.pie(filtered_df, values='Launch Site', 
        # names='class', 
        title='Launch success ratio for ' + entered_site)
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site, payload):
    print(payload)
    data = spacex_df[spacex_df['Payload Mass (kg)'] > payload[0]]
    data = data[data['Payload Mass (kg)'] < payload[1]]
    if entered_site == 'ALL':
        fig = px.scatter(data, y='class', 
        x='Payload Mass (kg)', 
        color="Booster Version Category",
        title='Payload vs. Launch Outcome for all sites')
        return fig
    else:
        filtered_df = data[data['Launch Site'] == entered_site]
        print(filtered_df.head())
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', 
        y='class', 
        color="Booster Version Category",
        title='Payload vs. Launch Outcome for ' + entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
