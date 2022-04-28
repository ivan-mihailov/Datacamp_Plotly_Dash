import pandas as pd
import plotly.express as px

ecom_sales = pd.read_csv('usr/local/share/datasets/ecom_sales.csv')
ecom_sales = ecom_sales.groupby('Country')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')

# Create the bar graph object
bar_fig = px.bar(
    # Set the appropriate DataFrame and title
    data_frame=ecom_sales,
    title='Total Sales by Country',
    # Set the x and y arguments
    x='Total Sales ($)',
    y='Country',
    # Ste the graph to be horizontal
    orientation = 'h')

# Increase the gap between bars
bar_fig.update_layout({'bargap' : 0.5})

bar_fig.show()
