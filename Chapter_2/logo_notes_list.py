import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_category = ecom_sales.groupby(['Major Category', 'Minor Category']).size(). \
    reset_index(name='Total orders').sort_values(by='Total Orders', ascending=False). \
    reset_index(drop=True)
num1_cat, num1_salesvol = ecom_category.loc[0].tolist()[1:3]
num2_cat, num2_salesvol = ecom_category.loc[1].tolist()[1:3]
ecom_bar = px.bar(data_frame=ecom_category, x='Total Orders', y='Minor Category',
                  color='Major Category')
ecom_bar.update_layout({'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'}})

# Create the dash app
app = dash.Dash()

# Set up the layout using an overall div
app.layout = html.Div([
        html.Img(src=logo_link),
        html.H1('Top Sales Categories'),
        # Add a div containing the bar figure
        html.Div(dcc.Graph(figure=ecom_bar)),
        # Add an overall text-containing component
        html.Span(children=[
            'The top 2 sales categories were:',
            # Set up an ordered list
            html.Ol(children=[
                # Add two list elements with the top category variables
                html.Li(children=[num1_cat, ' with ', num1_salesvol, ' sales volume']),
                html.Li(children=[num2_cat, ' with ', num2_salesvol, ' sales volume'])
            ], style={'width':'350px', 'margin':'auto'}),
            # Add a line break before the copyright notice
            html.Br(),
            # Italicize copyright notice
            html.I(' Copyright E-Com INC')])
    ],
    style={'text-align': 'center', 'font-size': 22})

if __name__ == '__main__':
    app.run_server(debug=True)
