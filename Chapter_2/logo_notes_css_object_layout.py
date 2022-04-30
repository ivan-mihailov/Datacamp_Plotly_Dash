import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_bar_major_cat = ecom_sales.groupby('Major Category')['OrderValue'].\
    agg('sum').reset_index(name='Total Sales ($)')
ecom_bar_minor_cat = ecom_sales.groupby('Minor Category')['OrderValue'].\
    agg('sum').reset_index(name='Total Sales ($)')
bar_fig_major_cat = px.bar(ecom_bar_major_cat, x='Total Sales ($)',
                           y='Major Category', color='Major Category',
                           color_discrete_map={'Clothes': 'blue',
                                               'Kitchen': 'red',
                                               'Garden': 'green',
                                               'Household': 'yellow'})
bar_fig_minor_cat = px.bar(ecom_bar_minor_cat, x='Total Sales ($)',
                           y='Minor Category')

# Create the dash app
app = dash.Dash()

app.layout = html.Div([
    html.Img(src=logo_link,
             # Add margin to the logo
             style={'margin': '30px 0px 0px 0px'}),
    html.H1('Sales breakdowns'),
    html.Div(children=[
        dcc.Graph(
            # Style the graphs to appear side-by-side
            figure=bar_fig_major_cat,
            style={'display': 'inline-block'}),
        dcc.Graph(
            figure=bar_fig_minor_cat,
            style={'display': 'inline-block'}),
    ]),
    html.H2('Major Category',
            # Style the titles to appear side-by-side with 2 pixel border
            style={'display': 'inline-block', 'border': '2px solid black',
            # style the titles to have the correct spacings
                   'padding': '10px', 'margin': '10px 220px'}),
    html.H2('Minor Category',
            # Style the titles to appear side-by-side with 2 pixel border
            style={'display': 'inline-block', 'border': '2px solid black',
                   # style the titles to have the correct spacings
                   'padding': '10px', 'margin': '10px 220px'}),
],
    style={'text-align': 'center', 'font-size': 22)

if __name__ == '__main__':
    app.run_server(debug=True)
