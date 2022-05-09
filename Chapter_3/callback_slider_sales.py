import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_sales['InvoiceDate'] = pd.to_datetime(ecom_sales['InvoiceDate'])

# Create the dash app
app = dash.Dash()

app.layout = html.Div([
    html.Img(src=logo_link, style={'margin': '30px 0px 0px 0px'}),
    html.H1('Sales breakdowns'),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H2('Controls'),
                    html.Br(),
                    html.H3('Minimum OrderValue Select'),
                    # Add a slider input
                    dcc.Slider(id='value_slider',
                               # Set the min and max of the slider
                               min=ecom_sales['OrderValue'].min(),
                               max=ecom_sales['OrderValue'].max(),
                               # Start the slider at 0
                               value=0,
                               # Increment the slider by 50 each notch
                               step=50,
                               vertical=False)
                ],
                style={'width': '350px', 'height': '350px', 'display': 'inline-block',
                       'vertical-align': 'top', 'border': '1px solid black',
                       'padding': '20px'}),
            html.Div(children=[
                # Add a graph component with identifier
                dcc.Graph(id='sales_cat'),
                html.H2('Sales by Major Category',
                        style={'border': '2px solid black', 'width': '200px',
                               'margin': '0 auto'})
            ],
                style={'width': '700px', 'display': 'inline-block'}),
        ])],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})


@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='sales_cat', component_property='figure'),
    Input(component_id='value_slider', component_property='value')
)
def update_plot(min_val):
    sales = ecom_sales.copy(deep=True)
    if min_val:
        sales = sales[sales['OrderValue'] >= min_val]

    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue']. \
        size().reset_index(name='Total Sales Volume')

    bar_fig_major_cat = px.bar(title=f'Sales with order value: {min_val}',
                               data_frame=ecom_bar_major_cat,
                               orientation='h', x='Total Sales Volume',
                               y='Major Category')
    return bar_fig_major_cat


if __name__ == '__main__':
    app.run_server(debug=True)
