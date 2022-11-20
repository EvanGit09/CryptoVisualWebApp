from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df
import plotly.graph_objs as go
import time

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

        #print(fig_html)

        '''w = 12 * 60 * 60 * 1000
        #print(result_df)
        TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

        title = 'EUR to USD chart'

        #p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=700, plot_height=500, title = title)
        p = figure(x_axis_type="datetime", tools=TOOLS, width=700, height=500, title = title)
        p.xaxis.major_label_orientation = pi / 4
        
        p.grid.grid_line_alpha = 0.3
        
        p.segment(result_df.date_formatted, result_df.high, result_df.date_formatted, result_df.low, color="black")
        p.vbar(result_df.date_formatted[increasing], w, result_df.open[increasing], result_df.close[increasing],
            fill_color="#D5E1DD", line_color="black"
        )
        p.vbar(result_df.date_formatted[decreasing], w, result_df.open[decreasing], result_df.close[decreasing], 
            fill_color="#F2583E", line_color="black"
        )

        script, div = components(p)'''
        

        #return render(request,'pages/base.html',{'script':script, 'div':div })
        return render(request,'pages/base.html',context={'fig':fig_html })

        time.sleep(1)
