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
    dcc.Dropdown(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in allOptions['America']],
        multi=True
    ),
    html.Div(
        id='what-happend'
    )
])

@app.callback(
    output=Output('what-happend', 'children'),
    inputs=[Input('dropdown-a', 'value')]
)
def whatHappend(selected):
    return '{}'.format(selected)



if __name__ == '__main__':
    app.run_server(debug=True)
