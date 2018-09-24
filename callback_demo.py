# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()
app.title = 'Dash learning'

app.layout = html.Div(children=[
html.H3(children='demo'),

html.Label(children='Hours per Day'),
    dcc.Slider(id='hours', value=5, min=0, max=24, step=1),

html.Label(children='Rate'),
    dcc.Input(id='rate', value=2, type='number'),

html.Label(children='Amount per Day', id='apd'),
    html.Div(id='amount'),

html.Label(children='Amount per Week'),
    html.Div(id='amount-per-week')
])

@app.callback(output=dash.dependencies.Output('amount', 'children'),
    inputs=[dash.dependencies.Input('hours', 'value'),
        dash.dependencies.Input('rate', 'value')])
def compute_amount(hours, rate):
    return float(hours) * float(rate)

@app.callback(output=dash.dependencies.Output('amount-per-week', 'children'),
    inputs=[dash.dependencies.Input('amount', 'children')])
def compute_amount_week(amount):
    return float(amount) * 7

if __name__ == '__main__':
    app.run_server(debug=True)
