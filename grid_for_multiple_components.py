# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import pyodbc

conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=pc1134\sqlserver2018;DATABASE=sales;UID=sa;PWD=123654')
sql = "select tb as 表名, duedate as 截止日期, _rows as 行数\
 from v_db_overview\
 order by tb asc, duedate desc"
df = pd.read_sql(sql, conn)
conn.close()


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()
app.title = 'Multiple components'
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div(children=[

html.Div(children=[
    html.Div(children=[
        html.H2(id='h2', children='Dashboard')
    ], className = 'row'),
    html.Div(children=[
        html.Div(children=[
            dcc.Markdown(id='general_info',
            children='''
            这里是看板, 汇合了多个图表,表格等信息.
            1. 列表1
            2. 列表2
            3. 列表3
            ''')
        ], className = 'four columns'),
        html.Div(children=[
            dcc.Markdown(id='code_example',
            children='''
            **以下是sql例子**
            ```sql
            select id, name, city from person
            ```
            ''')
        ], className = 'four columns'),
        html.Div(children=[
            html.Div(id='quoted-text',
            children='''
                The children property is special.
                By convention, it's always the first
                attribute which means that you can
                omit it: html.H1(children='Hello Dash')
                is the same as html.H1('Hello Dash').
                Also, it can contain a string, a number,
                 a single component, or a list of components.
            ''')
        ], className = 'four columns'),
    ], className = 'row')
], className = 'row'),

html.Div(children=[
    html.Div(children=[
        generate_table(df)
    ], className = 'four columns'),
    html.Div(children=[
        dcc.Graph(id='bar-chart')
    ], className = 'four columns'),
    html.Div(children=[
        dcc.Graph(id='scatter-chart')
    ], className = 'four columns')
], className = 'row')
], className = 'ten columns offset-by-one')

@app.callback(
dash.dependencies.Output('bar-chart', 'figure'),
[dash.dependencies.Input('h2', 'children')]
)
def bar_chart(h2):
    traces = []
    traces.append(go.Bar(
        x = [1,2,3,4,5],
        y = [6,4,5,3,7],
        marker = {
            'color': 'orange'
        },
        opacity = .7
    ))
    return{
        'data': traces,
        'layout': go.Layout(
            title='条形图'
        )
    }

@app.callback(
dash.dependencies.Output('scatter-chart', 'figure'),
[dash.dependencies.Input('h2', 'children')]
)
def bar_chart(h2):
    traces = []
    colors = ['red', 'blue']
    y = [6,5,5.7,4.5,7]
    for c in colors:
        traces.append(go.Scatter(
            x = [1,2,3,4,5],
            y = y,
            marker={
                'size': 15,
                'color': c
            },
            opacity = .6,
            name = c
        ))
        y = [5,4,6.5,3,5]
    return{
        'data': traces,
        'layout': go.Layout(
            title='散点图'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
