import dash
from dash import html, dcc, Input, Output, callback


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'backgroundColor': '#1E1E2F'}, children=[
    html.H1('Global Meat Consumption Dashboard', style={'backgroundColor': '#1E1E2F','textAlign': 'center', 'color': '#fff', 'padding': '20px'}),
    html.Div([
        dcc.Graph(id='choropleth', style={'flex': 2}),
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=2011,
                max=2021,
                value=2021,
                marks={str(year): str(year) for year in range(2011, 2022)},
                step=1
            ),
            html.Div(id='info-card', style={'marginTop': '20px', 'textAlign' : 'center'}),
            dcc.Graph(id='pie-chart', style={'height': '300px', 'textAlign' : 'center'})
        ], style={'flex': 1, 'padding': '20px'})
    ], style={'display': 'flex', 'backgroundColor': '#1E1E2F'}),

    html.Div([
        dcc.Graph(id='bar-chart', style={'flex': 1}),
        dcc.Graph(id='line-chart', style={'flex': 1})
    ], style={'display': 'flex', 'backgroundColor': '#1E1E2F'})
])

if __name__ == '__main__':
    app.run(debug=True)