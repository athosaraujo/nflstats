from genericpath import exists
from dash import html, dcc, Input, Output
from matplotlib.pyplot import xlabel
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# Declares Litera as the light mode theme and Slate as the dark mode theme
url_theme1 = dbc.themes.LITERA
url_theme2 = dbc.themes.SLATE
template_theme1 = 'litera'
template_theme2 = 'slate'

# Reads the processed data, or in the case processedData is non existent, run dataTreat.py
if exists('processedData.csv'):
    df = pd.read_csv('processedData.csv')
else:
    exec(open('dataTreat.py').read())
    df = pd.read_csv('processedData.csv')


#Gathers the current active nfl teams from the dataFrame to be used in dropdown menus
current_teams = [{'label': x, 'value':x} for x in df['team'].unique()]#+ [{'label': 'All', 'value': 'All'}]

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            # Declares the button that switches between light and dark mode
            ThemeSwitchAIO (aio_id = 'theme', themes = [url_theme1, url_theme2]),
            html.H1('NFL Stats', style={'textAlign': 'center'}),
            # Dropdown menu that selects which teams are going to be processed into the first graph
            dcc.Dropdown(
                id = 'sel_teams',
                value = [team['label'] for team in current_teams[:2]],
                multi = True,
                options = current_teams
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            # Callback generated graph that returns a line chart with every selected team's player age
            dcc.Graph(id = 'age_graph')
        ])  
    ]),
    
            # This row consists of two pie chart graphs that return the top 10 colleges and hometowns amongst NFL player
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='college_pie_chart')
        ]),
        dbc.Col([
            dcc.Graph(id='hometown_pie_chart')
        ],),
    
    ],style={'margin-top':'25px','margin-bottom':'25px'}),

    dbc.Row([
        dbc.Col([
            # This column consists of a dropdown to select a single team to see the table
            html.H3('See full team info'),
            dcc.Dropdown(
                id = 'team01',
                value = current_teams[0]['value'],
                multi = False,
                options = current_teams
            )
        ]),
    ]), 
    dbc.Row([
        # This column returns the table with the selected team's information
        dbc.Col([], id='dTable')
    ])
])

# First Graph
@app.callback(
    Output('age_graph', 'figure'),
    Input('sel_teams', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value')
)
def line(sel_teams,toggle):
    # Makes a standalone dataFrame with only relevant information for the graph
    df2 = df[['playerName', 'age', 'team','id']].copy() 
    # Selects the graph theme based on the user's choice
    template = template_theme1 if toggle else template_theme2
    # Creates an index mask of user selected teams
    mask = df2['team'].isin(sel_teams)

    # Makes the line graph based on player Id and age, separating them by team
    fig = px.line(df2[mask], x="id", y="age", color='team')

    # Associates and replaces every player id with their name
    tick_labels = {player_id: player_name for player_id, player_name in df2[mask].set_index('id')['playerName'].items()}
    tick_labels_list = list(tick_labels.values())
    fig.update_xaxes(tickvals=df2[mask]['id'], ticktext=tick_labels_list,tickangle=90)

    # Stylizes the graph
    fig.update_traces(mode="markers+lines")
    fig.update_layout(
        template=template,
        xaxis_title="",
        yaxis_title="Age in years",
        title={
            'text' : "NFL Player ages sorted by team",
            'x':0.5,
            'xanchor': 'center'},
        height=800,
        width=1295
        )
    
    return fig

# Top 10 colleges pie chart
@app.callback(
    Output('college_pie_chart', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_college_pie_chart(toggle):
    template = template_theme1 if toggle else template_theme2
    college_counts = df['college'].value_counts()           # Selects all individual colleges
    college_counts_top10 = college_counts.head(10)          # Counts each instance
    college_pie = px.pie(                                   # Writes down the graph
        names=college_counts_top10.index,
        values=college_counts_top10.values,
        title='Top 10 Colleges with NFL Alumni',
        hole=.3
    )
    college_pie.update_layout(                              # Changes the pie chart theme and centralizes it's title
        template=template,
        title_x=0.5
    )
    return college_pie

# Hometown pie chart, follows pretty much the same logic behind the college one
@app.callback(
    Output('hometown_pie_chart', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_hometown_pie_chart(toggle):
    template = template_theme1 if toggle else template_theme2
    hometown_counts = df['hometown'].value_counts().head(10)
    hometown_pie = px.pie(
        names=hometown_counts.index, 
        values=hometown_counts.values, 
        title='Top 10 player hometowns', 
        hole=.3
        )
    hometown_pie.update_layout(template=template)
    hometown_pie.update_layout(
        template=template,
        title_x=0.5,  # Set title's x position to center
    )
    return hometown_pie

# The table callback
@app.callback(
    Output('dTable', 'children'),
    Input('team01', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)

def update_output(value, toggle):    
    
    # Copies the dataFrame and drops all irrelevant information
    dfT = df[df['team'] == value].copy()
    dfT.drop(['team', 'id'], inplace=True, axis=1)

    # Renames columns so they're more user friendly
    dfT.rename(
        columns={
            'playerName': 'Name',
            'age': 'Age',
            'hometown': 'Hometown',
            'college': 'College',
            'number': 'Number',
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'experience': 'Experience'
        }, inplace=True
    )

    # Light mode table
    if toggle:
        table = dash.dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in dfT.columns],
            data=dfT.to_dict('records'),
            style_table={'margin': 'left'},
            sort_action='native',  # Enable sorting by clicking
            sort_mode='single',
        )
    # Dark mode table
    else:
        table = dash.dash_table.DataTable(
            style_header={
                'backgroundColor': 'rgb(32, 35, 38)',
                'color': 'light grey'},
            style_data={
                'backgroundColor': 'rgb(52, 58, 64)',
                'color': 'light grey'},
            columns=[{"name": col, "id": col} for col in dfT.columns],
            data=dfT.to_dict('records'),
            sort_action='native',  # Enable sorting by clicking
            sort_mode='single'
        )
    return table



if __name__ == '__main__':
    app.run_server(debug = True, port='1251')