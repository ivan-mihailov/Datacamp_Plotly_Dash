import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import random
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('/usr/local/share/datasets/ecom_sales.csv')
major_categories = list(ecom_sales['Major Category'].unique())
minor_categories = list(ecom_sales['Minor Category'].unique())
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
ecom_country = ecom_sales.groupby('Country')['OrderValue'].agg(['sum', 'count']).reset_index().rename(
    columns={'count': 'Sales Volume', 'sum': 'Total Sales ($)'})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(src=logo_link,
             style={'margin': '30px 0px 0px 0px'}),
    html.H1('Sales breakdowns'),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H2('Controls'),
                    html.Br(),
                    html.H3('Major Category Select'),
                    dcc.Dropdown(
                        id='major_cat_dd',
                        options=[{'label': category, 'value': category} for category in major_categories],
                        style={'width': '200px', 'margin': '0 auto'}),
                    html.Br(),
                    html.H3('Minor Category Select'),
                    dcc.Dropdown(
                        id='minor_cat_dd',
                        style={'width': '200px', 'margin': '0 auto'})
                ],
                style={'width': '350px', 'height': '350px', 'display': 'inline-block',
                       'vertical-align': 'top', 'border': '1px solid black', 'padding': '20px'}),
            html.Div(
                children=[
                    dcc.Graph(id='sales_line'),
                    html.H3(id='chosen_major_cat_title')
                ],
                style={'width': '700px', 'height': '650px', 'display': 'inline-block'})
        ]), ],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})


# One callback to set minor values & HTML output
@app.callback(
    Output('minor_cat_dd', 'options'),
    Output('chosen_major_cat_title', 'children'),
    Input('major_cat_dd', 'value'))
def update_minor_dd(major_cat_dd):
    major_minor = ecom_sales[['Major Category', 'Minor Category']].drop_duplicates()
    relevant_minor_options = major_minor[major_minor['Major Category'] == major_cat_dd][
        'Minor Category'].values.tolist()
    minor_options = [{'label': x, 'value': x} for x in relevant_minor_options]

    if not major_cat_dd:
        major_cat_dd = 'None Selected'
    # Creating string for title
    major_cat_title = f'This is in the Major Category of : {major_cat_dd}'

    # Return the options and title
    return minor_options, major_cat_title


# Create a callback to set a default minor category value
@app.callback(
    Output('minor_cat_dd', 'value'),
    Input('minor_cat_dd', 'options'))
def select_minor_cat(options):
    chosen_val = 'None'
    if options:
        vals = [x['value'] for x in options]
        chosen_val = random.choice(vals)
    return chosen_val


@app.callback(
    Output('sales_line', 'figure'),
    Input('minor_cat_dd', 'value'))
def update_line(minor_cat):
    minor_cat_title = 'All'
    ecom_line = ecom_sales.copy()

    if minor_cat:
        minor_cat_title = minor_cat
        ecom_line = ecom_line[ecom_line['Minor Category'] == minor_cat]

    ecom_line = ecom_line.groupby('Year-Month')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    line_graph = px.line(ecom_line, x='Year-Month', y='Total Sales ($)',
                         title=f'Total Sales by Month for Minor Category: {minor_cat_title}')

    return line_graph


if __name__ == '__main__':
    app.run_server(debug=True)