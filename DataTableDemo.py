import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_table_experiments as dt
import pandas as pd
import pyodbc


conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=sales;UID=sa;PWD=123654')
sql1 = "SELECT year(sjfhrq) as year, xsdqms, xsbscms, hyms, cpxms, sum(hsje_bb) as amount, AVG(hsje_bb) as amount_avg from zsd013 where xsdqms != '' and xsbscms != '' and hyms != '' and cpxms != '' group by year(sjfhrq), xsdqms, xsbscms, hyms, cpxms"
df1 = pd.read_sql(sql1, conn)
conn.close()
df1=df1.round({'amount': 0, 'amount_avg': 0})
years=df1['year'].unique()
region=df1['xsdqms'].unique()
office=df1['xsbscms'].unique()
dfa = df1[['xsdqms', 'xsbscms']].drop_duplicates()
# {大区:[办事处]}
dq = dfa['xsdqms'].unique()
d1={}
l1=[]
for i in dq:
    for bsc in dfa[dfa['xsdqms'] == i]['xsbscms'].unique():
        l1.append(bsc)
    d1[i] = l1
    l1 = []
allOptions = d1


app = dash.Dash()

app.layout = html.Div([
    html.H1(
        '各维度销货统计'
    ),

    html.Div([
        html.Div([
            html.Label([
                '年份'
            ])
        ],style={'display': 'inline-block',
                'vertical-align': 'center'}
        ),
        html.Div([
            dcc.Dropdown(
                id='dropdown-year',
                options=[{'label': i, 'value': i} for i in years],
                multi=True,
                style={'display': 'inline-block',
                        'width': '500'}
            )
        ],style={'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([
            html.Label([
                '大区'
            ])
        ],style={'display': 'inline-block',
                'vertical-align': 'center'}
        ),
        html.Div([
            dcc.Dropdown(
                id='dropdown-region',
                options=[{'label': i, 'value': i} for i in region],
                multi=True,
                clearable=True,
                placeholder='大区',
                style={'display': 'inline-block',
                        'width': '500'}
            )
        ],style={'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([
            html.Label([
                '办事处'
            ])
        ],style={'display': 'inline-block',
                'vertical-align': 'center'}
        ),
        html.Div([
            dcc.Dropdown(
                id='dropdown-office',
                options=[],
                value=[],
                multi=True,
                clearable=True,
                placeholder='办事处',
                style={'display': 'inline-block',
                        'width': '500'}
            )
        ],style={'display': 'inline-block'})
    ]),

    html.Div(
        id='truth'
    ),
    html.Div(
        id='df'
    ),

    dt.DataTable(
        id='data-table',
        rows=[{}],
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[]
    )
])


#show truth
@app.callback(
    output=Output('truth', 'children'),
    inputs=[Input('dropdown-office', 'value')]
)
def show_truth(selected):
    return '{}'.format(selected)

# 根据大区更新办事处
@app.callback(
    output=Output('dropdown-office', 'options'),
    inputs=[Input('dropdown-region', 'value')]
)
def update_office_options(selected_region):
    officeList = []
    options = []
    if selected_region:
        for region in selected_region:
            l1 = allOptions[region]
            for office in l1:
                officeList.append(office)
        options = [{'label': i, 'value': i} for i in officeList]
    else:
        options = []
    return options


# 根据办事处更新datatable
@app.callback(
    output=Output('data-table', 'rows'),
    inputs=[Input('dropdown-office', 'value')]
)
def update_dt(selected_office):
    df_filtered = df1.drop(labels=df1.index, axis=0)
    for office in selected_office:
        df_filtered=df_filtered.append(other=df1[df1['xsbscms'] == office])
    return df_filtered.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
