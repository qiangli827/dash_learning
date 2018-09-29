import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = dash.Dash()

allOptions = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}

app.layout = html.Div([
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in allOptions.keys()],
        value='America'
    ),
    html.Div(
        id='output-a'
    ),

    html.Hr(),

    dcc.RadioItems(
        id='cities-dropdown'
    ),

    html.Hr(),

    html.Div(
        id='display-selected-values'
    ),

    html.H1(
        children=['what happend']
    ),
    html.Div(
        id='what-happend'
    ),
    html.H1(
        children=['the first']
    ),
    html.Div(
        id='the-first'
    ),
    html.H1(
        children=['comment']
    ),
    html.Div(
        id='comment'
    )
])


@app.callback(
    output=Output('cities-dropdown', 'options'),
    inputs=[Input('countries-dropdown', 'value')]
)
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in allOptions[selected_country]]

@app.callback(
    output=Output('cities-dropdown', 'value'),
    inputs=[Input('cities-dropdown', 'options')]
)
def theFirst(options):
    return options[0]['value']

@app.callback(
    output=Output('what-happend', 'children'),
    inputs=[Input('cities-dropdown', 'options')]
)
def whatHappend(options):
    return '{}'.format(options)
@app.callback(
    output=Output('the-first', 'children'),
    inputs=[Input('cities-dropdown', 'options')]
)
def theFirst(options):
    return options[0]['value']
@app.callback(
    output=Output('comment', 'children'),
    inputs=[
        Input('countries-dropdown', 'value'),
        Input('cities-dropdown', 'value')
    ]
)
def comment(country, city):
    return '{} is a city of {}.'.format(city, country)




if __name__ == '__main__':
    app.run_server(debug=True)
