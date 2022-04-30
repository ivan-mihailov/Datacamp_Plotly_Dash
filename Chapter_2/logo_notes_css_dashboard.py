import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_line = ecom_sales.groupby('Year-Month')['OrderValue'].agg('sum'). \
    reset_index(name='TotalSales')
line_fig = px.line(data_frame=ecom_line, x='Year-Month', y='TotalSales',
                title='Total Sales by Month')
line_fig.update_layout({'paper_bgcolor': 'rgb(224, 255, 252)'})
ecom_bar = ecom_sales.groupby('Country')['OrderValue'].agg('sum').\
    reset_index(name='TotalSales')
bar_fig = px.bar(data_frame=ecom_bar, x='TotalSales', y='Country',
                 orientation='h', title='Total Sales by Country')
bar_fig.update_layout({'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'},
                       'paper_bgcolor': 'rgb(224, 255, 252)'})

# Create the dash app
app = dash.Dash()

# Set up the layout using an overall div
app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(src=logo_link,
        # Place the logo side-by-side the H1 with required margin
        style={'display': 'inline-block, 'margin': '25px'}),
        html.H1(children=['Sales Figures'],
                # Make the H1 side-by-side with the logos
                style={'display': 'inline-block'}),
        html.Img(src=logo_link,
                 # Place the logo side-by-side the H1 with the required margin
                style={'display': 'inline-block', 'margin': '25px'})]),
    html.Div(
        dcc.Graph(figure=line_fig),
        # Ensure graphs are the correct size, side-by-side with required margin
        style={'width': '500px', 'display': 'inline-block', 'margin': '5px'}),
    html.Div(
        dcc.Graph(figure=bar_fig),
        # Ensure graphs are the correct size, side-by-side with required margin
        style={'width': '350px', 'display': 'inline-block', 'margin': '5px'}),
    html.H3(f'The largest order quantity was {ecom_sales.Quantity.max()}')
],
    style={'text-align': 'center', 'font-size': 22, 'background-color': 'rgb(224, 255, 252)'})

if __name__ == '__main__':
    app.run_server(debug=True)
