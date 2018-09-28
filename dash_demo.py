#_*_ coding: utf-8 _*_

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pyodbc

# 连接sql server数据库
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=pc1134\sqlserver2018;DATABASE=sales;UID=sa;PWD=123654')
sql = " \
 select xsdqms_new, hyms, round(sum(hsje_bb),0) as hsjebb\
 from v_zsd013_2_3_zdkh a\
 where duedate='2018/9/18' \
 and xsdqms_new like '%大区%'\
 and hyms != ''\
 group by xsdqms_new, hyms\
"
df = pd.read_sql(sql, conn)
conn.close()

# 处理数据
x = df['xsdqms_new']
y = df['hsjebb']

app = dash.Dash()

app.layout = html.Div(children = [
	html.H1(children = 'Hello Dash'),
	
	html.Div(children = '''
		Dash: A web application framework for Python.
	'''),
	
	dcc.Graph(
	id='example-graph',
	figure={
		'data': [
			{'x': df[df['xsdqms_new'] == i]['hyms'],
             'y': df[df['xsdqms_new'] == i]['hsjebb'],
             'type': 'bar', 'name': i}
            for i in df['xsdqms_new'].unique()
		],
		'layout': {
			'title': 'Dash Data Visualization'
		}
	}
	)
	
])

if __name__ == '__main__':
    app.run_server(port=8050, debug=True) 
