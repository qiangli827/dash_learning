import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import pyodbc


conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=sales;UID=sa;PWD=123654')
sql1 = "SELECT year(sjfhrq) as year, xsdqms, xsbscms, hyms, sum(hsje_bb) as amount, sum(hsje_bb)/12 as amount_per_month from zsd013 where xsdqms != '' and xsbscms != '' and hyms != '' and cpxms != '' group by year(sjfhrq), xsdqms, xsbscms, hyms"
df1 = pd.read_sql(sql1, conn)
conn.close()
df1=df1.round({'amount': 0, 'amount_per_month': 0})
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

    dcc.Dropdown(
        id='dropdown-year',
        options=[{'label': i, 'value': i} for i in years],
        multi=False,
        placeholder='年份',
        style={'margin-top': '10px',
               'margin-bottom': '10px'}
    ),

    dcc.Dropdown(
        id='dropdown-region',
        options=[{'label': i, 'value': i} for i in region],
        multi=True,
        clearable=True,
        placeholder='大区',
        style={'margin-top': '10px',
               'margin-bottom': '10px'}
    ),

    dcc.Dropdown(
        id='dropdown-office',
        options=[],
        value=[],
        multi=True,
        clearable=True,
        placeholder='办事处',
        style={'margin-top': '10px',
               'margin-bottom': '10px'}
    ),

    # html.Div(
    #     id='truth'
    # ),

    dcc.Graph(
        id='graph-a',
        figure={
            'data': [
                {'x': df1[(df1['xsbscms'] == '石家庄办') & (df1['year'] == 2018)]['hyms'],
                 'y': df1[(df1['xsbscms'] == '石家庄办') & (df1['year'] == 2018)]['amount'],
                 'name': 'bar-a', 'type': 'bar'}
            ],
            'layout': {
                'title': 'simple graph'
            }
        },
        style={'margin-top': '20px',
              'border-style': 'dashed',
              'border-width': '5px',
              'border-color': 'lightgray'}
    ),

    html.Div([
        dt.DataTable(
            id='data-table',
            rows=[{}],
            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[]
        )
    ], style={'margin-top': '20px',
              'border-style': 'dashed',
              'border-width': '5px',
              'border-color': 'lightblue'})
])




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


# 根据下拉选择项更新图表
@app.callback(
    output=Output('graph-a', 'figure'),
    inputs=[
        Input('dropdown-office', 'value'),
        Input('dropdown-year', 'value')]
)
def update_graph_a(selected_office, selected_year):
    df_filtered = df1[(df1['year'] == selected_year)]
    traces = []
    office_name = []
    for office in selected_office:
        df_temp = df_filtered[df_filtered['xsbscms'] == office]
        traces.append(
            go.Bar(
                x=df_temp['hyms'],
                y=df_temp['amount'],
                name=office
            )
        )
        office_name.append(office)
    if selected_year is None or len(office_name) == 0:
        graph_title = ''
    else:
        t = ''
        for i in office_name:
            if i == office_name[0]:
                t = t + i
            else:
                t = t + ',' + i
        graph_title = '{}年{}行业销货'.format(selected_year, t)

    return {
        'data': traces,
        'layout': go.Layout(
            title = graph_title
        )
    }




# 根据下拉选择项更新datatable
@app.callback(
    output=Output('data-table', 'rows'),
    inputs=[
        Input('dropdown-region', 'value'),
        Input('dropdown-office', 'value'),
        Input('dropdown-year', 'value')]
)
def update_dt(selected_region, selected_office, selected_year):
    df_filtered = df1.drop(labels=df1.index, axis=0)
    for region in selected_region:
        for office in selected_office:
            # for year in selected_year:
            df_filtered=df_filtered.append(
                other=df1[(df1['xsdqms'] == region)
                         &(df1['xsbscms'] == office)
                         &(df1['year'] == selected_year)]
            )
    return df_filtered.to_dict('records')


# @app.callback(
#     output=Output('truth', 'children'),
#     inputs=[Input('dropdown-year', 'value')]
# )
# def show_truth(selected_year):
#     return '{}, {}'.format(selected_year, type(selected_year))




if __name__ == '__main__':
    app.run_server(debug=True)
