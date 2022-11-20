from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df
import plotly.graph_objs as go
import time
import plotly.express as px

# Create your views here.
def homepage(request):

    # main loop
    while True:

        # Use utils.py to get the data
        result = get_data('BTC', 'USDT', rate='1m')

        result_df = convert_to_df(result)

        # Deduce whether the trend is increasing = GREEN or decreasing = RED
        increasing = result_df.close > result_df.open
        decreasing = result_df.open > result_df.close

        # Declare plotly figure (go)
        fig=go.Figure()

        fig.add_trace(go.Candlestick(x=result_df.date_formatted,
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

        #fig.write_html('./mysite/templates/mysite/pages/figure.html')

        fig.write_html('./mysite/templates/mysite/pages/figure.html')

        fig_file = open('./mysite/templates/mysite/pages/figure.html', 'r')

        fig_html = fig_file.read()

        fig_file.close()

        return render(request,'pages/base.html',context={'fig':fig_html })

def liveprice(request):

    # main loop
    while True:

        # Use utils.py to get the data
        result = get_data('BTC', 'USDT', rate='1m')

        result_df = convert_to_df(result)
        print(result_df)

        fig2 = px.line(result_df, x='date_formatted', y='close', title='Line Graph of Price')

        #date      open      high       low     close        volume      date_formatted


        #fig.write_html('./mysite/templates/mysite/pages/figure.html')

        fig2.write_html('./mysite/templates/mysite/pages/figure2.html')

        fig2_file = open('./mysite/templates/mysite/pages/figure2.html', 'r')

        fig2_html = fig2_file.read()

        fig2_file.close()
        
        return render(request,'pages/base.html',context={'fig':fig2_html })

def liveprice2(request):
     result = get_live_data()

     pd.DataFrame