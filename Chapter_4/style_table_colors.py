import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash_table import DataTable, FormatTemplate
import pandas as pd
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('/usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
key_stats_tb = ecom_sales.groupby(['Country', 'Major Category', 'Minor Category'])['OrderValue'].agg(
    ['sum', 'count', 'mean']).reset_index().rename(
    columns={'count': 'Sales Volume', 'sum': 'Total Sales ($)', 'mean': 'Average Order Value ($)'})

money_format = FormatTemplate.money(2)
money_cols = ['Total Sales ($)', 'Average Order Value ($)']
data_cols = [x for x in key_stats_tb.columns if x not in money_cols]
d_columns = [{'name': x, 'id': x} for x in data_cols]
d_columns += [{'name': x, 'id': x,
               'type': 'numeric', 'format': money_format
               } for x in money_cols]

d_table = DataTable(
    columns=d_columns,
    data=key_stats_tb.to_dict('records'),
    cell_selectable=False,
    sort_action='native',
    filter_action='native',
    page_action='native',
    page_current=0,
    page_size=10,
    # Align all cell contents left
    style_cell=({'textAlign': 'left'}),
    # Style the background of money columns
    style_cell_conditional=[
        {
            'if':
                {'column_id': 'Total Sales ($)'},
            'background-color': 'rgb(252, 252, 184)', 'textAlign': 'center'},
        {
            'if':
                {'column_id': 'Average Order Value ($)'},
            'background-color': 'rgb(252, 252, 184)', 'textAlign': 'center'}
    ],
    # Style all headers
    style_header={'background-color': 'rgb(168, 255, 245)'},
    # Style money header columns
    style_header_conditional=[
        {
            'if':
                {'column_id': 'Total Sales ($)'},
            'background-color': 'rgb(252, 252, 3)'},
        {
            'if':
                {'column_id': 'Average Order Value ($)'},
            'background-color': 'rgb(252, 252, 3)'}
    ],

)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(src=logo_link,
             style={'margin': '30px 0px 0px 0px'}),
    html.H1('Sales Aggregations'),
    html.Div(
        children=[
            html.H2('Key Aggregations'),
            d_table
        ],
        style={'width': '850px', 'height': '750px', 'margin': '0 auto'}
    ),
],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'}
)

if __name__ == '__main__':
    app.run_server(debug=True)
