import dash
from dash import dash_table
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

#Read data - (raw data)
df = pd.read_csv('personPortrait_ENG.csv')
df_desc = df.describe().reset_index()


#Calculate freq
#freq_table = pd.crosstab(df['Person gender name'], 'no_of_genders')
#freq_table = freq_table/len(df)

#Define categorical Columns & numeric Columns
cat_columns=[i for i in df.columns if df.dtypes[i]=='object']
num_cols = df._get_numeric_data().columns


#For correlation matrix
df_corr = df.select_dtypes(include=np.number).corr()
x = list(df_corr.columns)
y = list(df_corr.index)
z = df_corr.values

fig_corr = ff.create_annotated_heatmap(
    z,
    x=x,
    y=y,
    annotation_text=np.around(z, decimals=2),
    hoverinfo='z',
    colorscale='Blues'
)

fig_corr.update_layout(width=1040,
                       height=500,
                       margin=dict(l=40, r=20, t=20, b=20),
                       paper_bgcolor='rgba(0,0,0,0)'
                       )



#Create sideBar
sidebar = html.Div([
    dbc.Row([
        html.P("Data Description"),
        dbc.Row([
        dash_table.DataTable(
            data=df_desc.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_desc.columns],
            #page_size=100,
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '50px', 'width': '100px', 'maxWidth': '500px',
                'whiteSpace': 'nowrap'
            },#grey-white Striped Rows
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(242, 242, 242)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            }
        )
        ]),
        html.P("Dataset View"),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=100,
            #fixed_columns={'headers':True, 'data':1},
            #style_cell={'textAlign': 'left'},
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '50px', 'width': '100px', 'maxWidth': '500px',
                'whiteSpace': 'nowrap'
            },#grey-white Striped Rows
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(242, 242, 242)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            }
        )

    ])
])

content = html.Div([
    dbc.Row([
        dbc.Col([
            html.P('Data Distribution Graph - Counts'),
            dcc.Graph(
                id='example-graph'
            )
        ]),
        dbc.Col([
            html.P('Data Distribution Graph - Frequencies'),
            dcc.Graph(
                id='freqPlot'
            )
        ],style={"height":"45vh"}) #to style ayto allazei to ipsos toy corr title
    ]),
    dbc.Row([
        html.P('Correlation Matrix'),
        dcc.Graph(
                id='cormatrix',
                figure=fig_corr
            )
    ])
])

app.layout = dbc.Container(
    [
        html.H1("Dashboard - Data Exploration",style={'textAlign': 'center'}),
        html.Hr(),
        html.P('Please select a column below:',style={'font-size':'25px'}),
        dcc.Dropdown(df.columns, id='dropdown1'),
        html.Br(),
        dbc.Row([
            dbc.Col(sidebar, width=4, className='bg-light'),
            dbc.Col(content, width=7)#9
        ])
    ],
    fluid=True
    )

#Create plot for frequencies
@app.callback(
    Output('freqPlot', 'figure'),
    Input('dropdown1', 'value')
)

def generate_freq_plot(value):

    freq_table = pd.crosstab(df[value], 'no_of_items')
    freq_table = freq_table / len(df)

    fig_freq = px.bar(freq_table,
                       title='Data distribution - Frequencies',
                       #color=df['Person gender name'],
                       height=500
                       )
    return fig_freq



#Create plot for counts
@app.callback(
    Output('example-graph', 'figure'),
    [Input('dropdown1', 'value')]
)

def update_figure(value):

    fig = px.histogram(df,x=value,
                       title='Data distribution',color=df['Person gender name'],
                       height=500,
                       histfunc="count")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)