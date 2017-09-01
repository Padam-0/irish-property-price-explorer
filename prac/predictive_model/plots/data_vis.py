"""
File to trial making plots using plotly
"""
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

df = pd.read_csv('../model_data_model_split.csv', encoding='latin1', index_col=0)
print('Data imported...')


data = [go.Bar(
            x=['giraffes', 'orangutans', 'monkeys'],
            y=[20, 14, 23]
    )]

py.plot(data, filename='basic-bar')



# btc_trace = go.Scatter(x=btc_usd_price_kraken.index, y=btc_usd_price_kraken['Weighted Price'])
# py.iplot([btc_trace])