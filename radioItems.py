import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in ['Canada', 'USA', 'Mexico']],
        value='Canada'
    ),
    html.Div(
        id='div1'
    ),

])

@app.callback(
    output=dash.dependencies.Output('div1', 'children'),
    inputs=[dash.dependencies.Input('dropdown-a', 'value')]
)
def show_selected(selectedItem):
    return 'You\'ve selected {}.'.format(selectedItem)

if __name__ == '__main__':
    app.run_server(debug=True)
