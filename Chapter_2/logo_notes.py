import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_bar = ecom_sales.groupby('Country')['OrderValue'].agg('sum'). \
    reset_index(name='Total Sales ($)').sort_values(by='Total Sales ($)',
                                                    ascending=False)
top_country = ecom_bar.loc[0]['Country']
bar_fig_country = px.bar(data_frame=ecom_bar, x='Total Sales ($)', y='Country',
                         color='Country', color_discrete_map=
                         {'United Kingdom': 'lightblue', 'Germany': 'orange',
                          'France': 'darkblue', 'Australia': 'green',
                          'Hong Kong': 'red'})

# Create the dash app
app = dash.Dash()

# Set up the layout using an overall div
app.layout = html.Div(
    children=[
        html.Img(src=logo_link),
        html.H1('Sales by Country'),
        # Add a div containing the bar figure
        html.Div(dcc.Graph(figure=bar_fig_country), style={'width': '750px',
                                                           'margin': 'auto'}),
        # Add an overall text-containing component
        html.Span(children=[
            # Add the top country text
            'This year, the most sales came from: ',
            html.B(top_country),
            # Italicize copyright notice
            html.I(' Copyright E-Com INC')])
    ],
    style={'text-align': 'center', 'font-size': 22})

if __name__ == '__main__':
    app.run_server(debug=True)
