import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime, date

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_sales['InvoiceDate'] = pd.to_datetime(ecom_sales['InvoiceDate'])

# Create the dash app
app = dash.Dash()


# Create a reusable component function called add_logo
def add_logo():
    # Add a component that will render an image
    corp_logo = html.Img(
        src=logo_link,
        # Add the corporate styling
        style={'margin': '20px 20px 5px 5px', 'border': '1px dashed lightblue',
               'display': 'inline-block'})

    return corp_logo


app.layout = html.Div([
    add_logo(),
    html.Br(),
    html.H1('Sales breakdowns'),
    html.Br(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    add_logo(),
                    html.H2('Controls', style={'margin': '0 10px',
                                               'display': 'inline-block'}),
                    add_logo(),
                    html.Br(),
                    html.H3('Sale Date Select'),
                    # Create a single date picker with identifier
                    dcc.DatePickerSingle(id='sale_date',
                                         # Set the min/max dates allowed as the min/max dates in the DataFrame
                                         min_date_allowed=ecom_sales['InvoiceDate'].min(),
                                         max_date_allowed=ecom_sales['InvoiceDate'].max(),
                                         # Set the initial visible date
                                         date=date(2011, 4, 11),
                                         initial_visible_month=date(2011, 4, 1),
                                         style={'width': '200px', 'margin': '0 auto'})
                ],
                style={'width': '350px', 'height': '350px', 'display': 'inline-block',
                       'vertical-align': 'top', 'border': '1px solid black',
                       'padding': '20px'}),
            html.Div(children=[
                # Add a graph component with identifier
                dcc.Graph(id='sales_cat'),
                html.H2('Daily Sales by Major Category',
                        style={'border': '2px solid black', 'width': '200px',
                               'margin': '0 auto'})
            ],
                style={'width': '700px', 'display': 'inline-block'}),
        ]),
    add_logo()],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})


@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='sales_cat', component_property='figure'),
    Input(component_id='sale_date', component_property='date')
)
def update_plot(input_date):
    sales = ecom_sales.copy(deep=True)
    if input_date:
        sales = sales[sales['InvoiceDate'] == input_date]
    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue']. \
        agg('sum').reset_index(name='Total Sales ($)')
    bar_fig_major_cat = px.bar(title=f'Sales on {input_date}',
                               data_frame=ecom_bar_major_cat,
                               orientation='h', x='Total Sales ($)',
                               y='Major Category')
    return bar_fig_major_cat


if __name__ == '__main__':
    app.run_server(debug=True)
