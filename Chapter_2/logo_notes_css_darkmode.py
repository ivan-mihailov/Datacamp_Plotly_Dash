import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '1c95273e21a54b5ca48e0b03cc0c1faeafb3d7cd/e-comlogo_white.png'
ecom_category = ecom_sales.groupby(['Major Category', 'Minor Category']).size(). \
    reset_index(name='Total orders').sort_values(by='Total Orders', ascending=False). \
    reset_index(drop=True)
top_cat = ecom_category.loc[0]['Minor Category']
ecom_bar = px.bar(data_frame=ecom_category, x='Total Orders', y='Minor Category',
                  color='Major Category')

# Set the font color of the bar chart
ecom_bar.update_layout({'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'},
                        'paper_bgcolor': 'black', 'font': {'color': 'white'}})

# Create the dash app
app = dash.Dash()

# Set up the layout using an overall div
app.layout = html.Div([
    html.Img(src=logo_link,
             # Set the size of the logo
             style={'width': '165px', 'height': '50px'}),
    html.H1('Top Sales Categories'),
    # Set the size of the bar graph
    html.Div(dcc.Graph(figure=ecom_bar,
                       style={'width': '500px', 'height': '350px', 'margin': 'auto'})
             ),
    html.Br(),
    html.Span(children=[
        'The top category was: ',
        html.B(top_cat),
        html.Br(),
        # Italicize copyright notice
        html.I(' Copyright E-Com INC')])
    # Add a background color to the entire app
],
    style={'text-align': 'center', 'font-size': 22,
           # Update the background color to the entire app
           'background-color': 'black',
           # Change the text color for the whole app
           'color': 'white'})

if __name__ == '__main__':
    app.run_server(debug=True)
