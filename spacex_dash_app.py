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

# TASK 1: I  create a dropdown for Launch Site selection.
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
sites = spacex_df['Launch Site'].unique()
for site in sites:
    site_options.append({'label': site, 'value': site})

dropdown = dcc.Dropdown(id='site-dropdown',
                        options=site_options,
                        value='ALL',
                        placeholder="Select a Launch Site",
                        searchable=True)

# TASK 3: I  create a slider for Payload Range Selection.
slider = dcc.RangeSlider(id='payload-slider',
                         min=min_payload,
                         max=max_payload,
                         value=[min_payload, max_payload],
                         marks={i: '{}kg'.format(i) for i in range(int(min_payload), int(max_payload)+1000, 1000)},
                         step=100)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    dropdown,
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    slider,
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: I  create a callback to update the pie chart based on the Launch Site selection.
@app.callback(Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class', title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title='Success vs. Failed Launches for {}'.format(selected_site))
    return fig

# TASK 4: I  create a callback to update the scatter chart based on the Launch Site and Payload Range selection.
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            size='Payload Mass (kg)',title='Payload vs. Outcome based on selected criteria')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()