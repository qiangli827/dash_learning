import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from datetime import datetime as dt

app = dash.Dash()

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='date-picker-single',
        initial_visible_month=dt(2018,6,14),
        date=dt(2018,6,14),
        display_format='YYYY/M/D'
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)
