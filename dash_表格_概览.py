#_*_ coding: utf-8 _*_

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pyodbc

# 连接sql server数据库
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=pc1134\sqlserver2018;DATABASE=sales;UID=sa;PWD=123654')
sql = "declare @duedate date\
 set @duedate = (select max(duedate) from zsd013)\
 exec proc_ndq5w @duedate\
"
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

app.layout = html.Div(children=[
    html.H4(children='NDQ5W销售排行榜'),
    generate_table(df),
    html.H5(children='数据库概览2'),
    generate_table(df)
])


if __name__ == '__main__':
    app.run_server(debug=True)