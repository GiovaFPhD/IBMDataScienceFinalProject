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
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div([
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([ ], id='success-pie-chart'),
                                #html.Div([ ],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=2000,
                                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500',10000:'10000'
                                                    },
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Div([ ], id='success-payload-scatter-chart'),
                                ])
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='children'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(value):
    filtered_df = spacex_df
    if value == 'ALL':
        totalsucces=filtered_df['class'].sum()
        totalsucces
        data=filtered_df[['Launch Site','class']].groupby(['Launch Site']).sum()
        data.reset_index(inplace=True)
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return dcc.Graph(figure=fig)
    else:
        data=filtered_df[filtered_df['Launch Site']==value]
        data=data[['Flight Number','class']].groupby(['class']).count()
        data.reset_index(inplace=True)
        fig = px.pie(data, values='Flight Number', 
        names='class', 
        title='Total Success Launches for site {}'.format(value),)
        return dcc.Graph(figure=fig)
        
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='children'),
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )
def get_scatter_chart(site_value,payload_value):
    filtered_df = spacex_df
    if site_value == 'ALL':
        
        data=filtered_df[(filtered_df['Payload Mass (kg)']>=payload_value[0]) & (filtered_df['Payload Mass (kg)']<=payload_value[1])]
        #data=filtered_df[filtered_df['Payload Mass (kg)']==payload_value]
        #data.reset_index(inplace=True)
        fig2 = px.scatter(data, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return dcc.Graph(figure=fig2)
    else:
        data1=filtered_df[filtered_df['Launch Site']==site_value]
        #data=filtered_df[filtered_df['Launch Site']==value]
        data=data1[(data1['Payload Mass (kg)']>=payload_value[0]) & (data1['Payload Mass (kg)']<=payload_value[1])]
        fig2 = px.scatter(data, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return dcc.Graph(figure=fig2)
        

# Run the app
if __name__ == '__main__':
    app.run_server()
