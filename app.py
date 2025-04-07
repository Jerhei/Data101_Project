import dash
from dash import html, dcc, Input, Output, callback


app = dash.Dash(__name__)
server = app.server

meat_types = ['Poultry', 'Beef', 'Pork', 'Sheep and goat', 'Fish and seafood', 'Other meats']
#meat_colors = ['#B4EDD2', '#A0CFD3', '#9A7AA0', '#BD94BA', '#87677B', '#CC99FF']
meat_colors = ['#d98e73', '#ffb5a7', '#fcd5ce', '#f8edeb', '#f9dcc4', '#fec89a']


# Callback to update all graphs based on year and country
@app.callback(
    [Output('choropleth', 'figure'),
     Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('info-card', 'children')],
    [Input('year-slider', 'value'),
     Input('choropleth', 'clickData')]
)
def update_charts(selected_year, click_data):
    choropleth_data = df[df['Year'] == selected_year]

    # Get selected country from click data
    selected_country = click_data['points'][0]['location'] if click_data else choropleth_data['Country'].iloc[0]

    # Choropleth
    choropleth_fig = px.choropleth(
        choropleth_data,
        locations='Country',
        locationmode='country names',
        color='Total Consumption',
        hover_name='Country',
        title=f'Global Meat Consumption Per Capita in {selected_year}',
        color_continuous_scale='Reds'
    )
    choropleth_fig.update_layout(plot_bgcolor='#1E1E2F', paper_bgcolor='#1E1E2F', font_color='#fff')

    # Stacked Bar Chart
    top_countries = choropleth_data.groupby('Country')[meat_types].sum().nlargest(10, 'Poultry')
    bar_fig = px.bar(
        top_countries,
        x=top_countries.index,
        y=meat_types,
        title=f'Top 10 Consumer Countries in {selected_year}',
        labels={'value': 'Meat Consumption (kg per capita)', 'x': 'Country'},
        barmode='stack',
        color_discrete_sequence=px.colors.sequential.Reds
    )

    import textwrap

    def wrap_labels(labels, width=10):
        return ['<br>'.join(textwrap.wrap(label, width=width)) for label in labels]

    bar_fig.update_layout(plot_bgcolor='#1E1E2F', paper_bgcolor='#1E1E2F', font_color='#fff', barmode='stack', bargap=0.1, margin=dict(l=50, r=50, t=50, b=50),
                          xaxis=dict(
                          tickvals=top_countries.index, tickfont=dict(size=9),
                          ticktext=wrap_labels(top_countries.index, width=10),
                          tickangle=0
                                    )
                          )

    # Line Chart
    df_filtered2 = df[df['Year'].between(1961, selected_year)]
    df_grouped = df_filtered2.groupby('Year')[meat_types].mean()
    line_fig = px.line(
        df_grouped,
        x=df_grouped.index,
        y=meat_types,
        title='Consumption Trends Over Time',
        labels={'value': 'Average Consumption (kg per capita)', 'Year': 'Year'}
    )
    line_fig.update_layout(plot_bgcolor='#1E1E2F', paper_bgcolor='#1E1E2F', font_color='#fff')

    # Donut Chart
    country_data = choropleth_data[choropleth_data['Country'] == selected_country]
    if not country_data.empty:
        df_year = country_data[meat_types].iloc[0]
        pie_fig = px.pie(
            names=meat_types,
            values=df_year,
            title=f'{selected_country} Meat Consumption in {selected_year}',
            color=meat_types,
            color_discrete_sequence=meat_colors,
            hole=0.4
        )
        pie_fig.update_layout(plot_bgcolor='#1E1E2F', paper_bgcolor='#1E1E2F', font_color='#fff')

        total_consumption = f"{country_data.iloc[0]['Total Consumption'] / 1000:.2f}K"
        info_card = html.Div([
            html.H2(selected_country, style={'color': '#fff'}),
            html.P("Country", style={'color': '#ccc'}),
            html.Div([
                html.Div([
                    html.H3(total_consumption, style={'color': '#fff'}),
                    html.P("Total Consumption", style={'color': '#ccc'})
                ], style={'display': 'inline-block', 'width': '48%'}),
                html.Div([
                    html.H3(selected_year, style={'color': '#fff'}),
                    html.P("Year", style={'color': '#ccc'})
                ], style={'display': 'inline-block', 'width': '48%'})
            ])
        ])
    else:
        pie_fig = go.Figure()
        info_card = html.Div([html.H2("No Data"), html.P("No data available for the selected country or year")])

    return choropleth_fig, bar_fig, line_fig, pie_fig, info_card

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