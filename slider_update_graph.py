# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)

app = dash.Dash()

app.title = 'slider update graph'

app.layout = html.Div([
    dcc.Graph(
        id='graph-with-slider'
    ),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])

@app.callback(
    output = Output('graph-with-slider', 'figure'),
    inputs = [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    df_filtered = df[df['year'] == selected_year]
    traces = []
    for i in df_filtered.continent.unique():
        df_continent = df_filtered[df_filtered['continent'] == i]
        traces.append(go.Scatter(
            x=df_continent['gdpPercap'],
            y=df_continent['lifeExp'],
            text=df_continent['country'],
            mode='markers',
            opacity=.7,
            marker={
                'size': 15,
                'line': {'width': .5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
