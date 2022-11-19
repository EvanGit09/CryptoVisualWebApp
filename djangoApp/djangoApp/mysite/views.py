from django.shortcuts import render
#from bokeh.plotting import figure, output_file, show
#from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df
import plotly.graph_objs as go 

# Create your views here.
def homepage(request):

    # Use utils.py to get the data
    result = get_data('BTC', 'USDT', rate='30m')

    result_df = convert_to_df(result)

    # Deduce whether the trend is increasing = GREEN or decreasing = RED
    increasing = result_df.close > result_df.open
    decreasing = result_df.close > result_df.open

    # Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=result_df.index,
                    open=result_df['open'],
                    high=result_df['high'],
                    low=result_df['low'],
                    close=result_df['close'], name = 'market data'))

    fig.update_layout(
        title= 'BTC/USD',
        yaxis_title='Price')               

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    script, div = components(fig)

    return render(request,'pages/base.html',{'script':script, 'div':div })
