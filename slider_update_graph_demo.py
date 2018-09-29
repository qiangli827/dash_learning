# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import pyodbc
import plotly.graph_objs as go

conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=sales;UID=sa;PWD=123654')
sql1 = "SELECT year(sjfhrq) as year, xsdqms, xsbscms, hyms, cpxms, sum(hsje_bb) as amount\
 from zsd013\
 where xsdqms != '' and xsbscms != '' and hyms != '' and cpxms != ''\
  and cpxms != '品牌柜产品线'\
 group by year(sjfhrq), xsdqms, xsbscms, hyms, cpxms\
 order by hyms, cpxms"
df = pd.read_sql(sql1, conn)
conn.close()
df = df[df['amount'] >= 0]

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
    for i in df_filtered.xsdqms.unique():
        df_dq = df_filtered[df_filtered['xsdqms'] == i]
        traces.append(go.Scatter(
            x=df_dq['hyms'],
            y=df_dq['cpxms'],
            text=df_dq['amount'],
            mode='markers',
            opacity=.7,
            marker={
                'size': df_dq['amount'],
                'line': {'width': .5, 'color': 'white'},
                'sizemode': 'area',
                'sizeref': 2.*max(df_dq['amount'])/(40.**2)
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title': 'industry'},
            yaxis={'title': 'product line'},
            margin={'l': 100, 'b': 40, 't': 30, 'r': 40},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
