# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

app = dash.Dash()

app.title = 'check list'

app.layout = html.Div(children=[

html.H1(
    children='check list',
    style={
        'margin': '10px'
    }
),

dcc.Checklist(
    id='cities',
    options=[
        {'label': 'yangquan', 'value': 'yq'},
        {'label': 'taiyuan', 'value': 'ty'},
        {'label': 'beijing', 'value': 'bj'},
        ],
    values=['yq', 'bj'],
    style={
        'margin': '10px'
    }
),

html.Div(
    id='text',
    style={
        'margin': '10px'
    }
)

])

@app.callback(
    Output('text', 'children'),
    [Input('cities', 'values')]
)
def show_text(cities):
    num = len(cities)
    text = ''
    if num <= 1:
        text = 'You\'ve selected {} city.'.format(num)
    else:
        text = 'You\'ve selected {} cities.'.format(num)
    return text

if __name__ == "__main__":
    app.run_server(debug=True)
