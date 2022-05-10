import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/' \
            '2bac9433b0e904735feefa26ca913fba187c0d55/e_com_logo.png'
ecom_country = ecom_sales.groupby('Country')['OrderValue'].agg(['sum', 'count']).\
    reset_index().rename(columns={'count': 'Sales Volume', 'sum': 'Total Sales ($)'})
# Add the country data to the scatter plot
ecom_scatter = px.scatter(data_frame=ecom_country, x='Total Sales ($)',
                          y='Sales Volume', color='Country', width=350,
                          height=550, custom_data=['Country'])
ecom_scatter.update_layout({'legend': dict(orientation='h', y=-0.7, x=1,
                                           yanchor='bottom', xanchor='right')})

# Create the dash app
app = dash.Dash()

app.layout = html.Div([
    html.Img(src=logo_link, style={'margin': '30px 0px 0px 0px'}),
    html.H1('Sales breakdowns'),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H3('Sales Volume vs Sales Amount by Country'),
                    dcc.Graph(id='scatter', figure=ecom_scatter)
                ],
                style={'width':'350px', 'height':'650px', 'display':'inline-block',
                       'vertical-align':'top', 'border':'1px solid black',
                       'padding':'20px'}),
            html.Div(children=[
                dcc.Graph(id='major_cat'),
                dcc.Graph(id='minor_cat'),
                ],
                style={'width':'700px', 'height': '650px', 'display':'inline-block'}),
            ]),],
style={'text-align':'center', 'display':'inline-block', 'width':'100%'})

# Create a callback to update the minor category plot
@app.callback(
    Output('minor_cat', 'figure'),
    Input('scatter', 'hoverData'))
def update_min_cat_hover(hoverData):
    hover_country = 'Australia'

    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    minor_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    minor_cat_agg = minor_cat_df.groupby('Minor Category')['OrderValue'].\
        agg('sum').reset_index(name='Total Sales ($)')
    ecom_bar_minor_cat = px.bar(minor_cat_agg, x='Total Sales ($)',
                                y='Minor Category', orientation='h', height=450,
                                title=f'Sales by Minor Category for: {hover_country}')
    ecom_bar_minor_cat.update_layout({'yaxis': {'dtick': 1,
                                                'categoryorder': 'total ascending'},
                                      'title': {'x': 0.5}})

    return ecom_bar_minor_cat

# Create a callback to update the major category plot
@app.callback(
    Output('major_cat', 'figure'),
    Input('scatter', 'hoverData'))
def update_major_cat_hover(hoverData):
    hover_country = 'Australia'

    # Conditionally select the country from the hover data
    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    major_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    major_cat_agg = major_cat_df.groupby('Major Category')['OrderValue'].\
        agg('sum').reset_index(name='Total Sales ($)')
    ecom_bar_major_cat = px.bar(major_cat_agg, x='Total Sales ($)',
                                y='Major Category', height=300,
                                title=f'Sales by Major Category for: {hover_country}',
                                color='Major Category',
                                color_discrete_map={'Clothes': 'blue',
                                                    'Kitchen': 'red',
                                                    'Garden': 'green',
                                                    'Household': 'yellow'})
    ecom_bar_major_cat.update_layout({'margin': dict(l=10, r=15, t=40, b=0),
                                      'title': {'x': 0.5}})

    return ecom_bar_major_cat

if __name__ == '__main__':
    app.run_server(debug=True)
