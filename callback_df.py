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

def update_dt(selected_office):
    df_filtered = df1.drop(labels=df1.index, axis=0)
    for office in selected_office:
        df_filtered=df_filtered.append(other=df1[df1['xsbscms'] == office])
    return df_filtered
