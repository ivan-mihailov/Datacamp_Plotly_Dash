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


# Create a reusable component for break lines
def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list


# Create a reusable component function called add_logo
def add_logo():
    # Add a component that will render an image
    corp_logo = html.Img(
        src=logo_link,
        # Add the corporate styling
        style={'margin': '20px 20px 5px 5px', 'border': '1px dashed lightblue',
               'display': 'inline-block'})
    return corp_logo


# Create a function to add corporate styling
def style_c():
    layout_style = {'display': 'inline-block', 'margin': '0 auto',
                    'padding': '20px'}
    return layout_style


app.layout = html.Div([
    add_logo(),
    # Insert 2 HTML break lines
    *make_break(2),
    html.H1('Sales breakdowns'),
    # Insert three HTML break lines
    *make_break(3),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H2('Controls', style=style_c()),
                    html.H3('Search Descriptions'),
                    *make_break(2),
                    # Add the required input
                    dcc.Input(id='search_desc', type='text',
                              placeholder='Filter Product Descriptions',
                              # Ensure input is triggered with 'Enter'
                              debounce=True,
                              # Ensure the plot can load without a selection
                              required=False,
                              style={'width': '200px', 'height': '30px'})
                ],
                style={'width': '350px', 'height': '350px', 'display': 'inline-block',
                       'vertical-align': 'top', 'border': '1px solid black',
                       'margin': '0px 80px'}),
            html.Div(children=[
                # Add a graph component with identifier
                dcc.Graph(id='sales_desc'),
                html.H2('Sales Quantity by Country',
                        style={'border': '2px solid black', 'width': '400px',
                               'margin': '0 auto'})
            ],
                style={'width': '700px', 'display': 'inline-block'}),
        ])],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})


@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='sales_desc', component_property='figure'),
    Input(component_id='search_desc', component_property='value')
)
def update_plot(search_value):
    title_value = 'None Selected (Showing all)'

    sales = ecom_sales.copy(deep=True)
    if search_value:
        sales = sales[sales['Description'].str.contains(search_value, case=False)]
        title_value = search_value

    fig = px.scatter(title=f'Sales with description text: {search_value}',
                     data_frame=sales,
                     x='Quantity',
                     y='OrderValue', color='Country')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
