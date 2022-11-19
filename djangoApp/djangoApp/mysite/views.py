from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df

# Create your views here.
def homepage(request):

    # Use utils.py to get the data
    result = get_data('BTC', 'USDT', rate='30m')

    result_df = convert_to_df(result)

    # Deduce whether the trend is increasing = GREEN or decreasing = RED
    increasing = result_df.close > result_df.open
    decreasing = result_df.close > result_df.open

    # 30 mins 
    w = 12 * 60 * 60 * 1000

    # Setup graph with bokeh
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    title = 'BTC to USD chart'

    p = figure(x_axis_type="datetime", tools=TOOLS, width=700, height=500, title = title)
    p.xaxis.major_label_orientation = pi / 4

    p.grid.grid_line_alpha = 0.3

    p.segment(result_df.index, result_df.high, result_df.index, result_df.low, color="black")

    # Set up colours
    p.vbar(result_df.index[increasing], w, result_df.open[increasing], result_df.close[increasing],
        fill_color="#D5E1DD", line_color="black"
    )
    p.vbar(result_df.index[decreasing], w, result_df.open[decreasing], result_df.close[decreasing], 
        fill_color="#F2583E", line_color="black"
    )

    script, div = components(p)

    return render(request,'pages/base.html',{'script':script, 'div':div })


