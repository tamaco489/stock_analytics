from pyti.bollinger_bands import upper_bollinger_band as bb_up
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from pyti.bollinger_bands import lower_bollinger_band as bb_low
import pandas_datareader.data as pdr
import talib as ta
import numpy as np
import plotly.graph_objs as pgo
import plotly.io as pio
import vars.stock as s

# Generate forecast analysis chart
def forecast_analysis(symbol):
    image_name = f'./data/08_forecast_analysis_chart_{symbol}.png'
    df = pdr.DataReader(s.symbol, s.finance, s.start, s.end).sort_index()

    close_data_list = df['Close'].tolist()                 # 終値をリスト型に変換
    close_data      = df['Close']                          # 終値を使用してSMA, MACD, RSIを計算

    # ----------------------------
    # BB
    # ----------------------------
    period = s.sma_middle_span                             # 中期EMAをmiddle_bandに指定
    upper_band, middle_band, lower_band = bb_up(close_data_list, period), bb_mid(close_data_list, period), bb_low(close_data_list, period)
    df['bb_up'], df['bb_mid'], df['bb_low'] = upper_band, middle_band, lower_band


    # ----------------------------
    # MACD
    # ----------------------------
    macd, macdsignal, _  = ta.MACD(
                                close_data,
                                fastperiod   = s.macd_short_span,
                                slowperiod   = s.macd_long_span,
                                signalperiod = s.macd_signal
                            )
    df['macd']        = macd
    df['macd_signal'] = macdsignal


    # ----------------------------
    # RSI
    # ----------------------------
    rsi_short = ta.RSI(
        close_data,
        timeperiod=s.rsi_short_span
    )

    rsi_long  = ta.RSI(
        close_data,
        timeperiod=s.rsi_long_span
    )

    df['rsi' + str(s.rsi_short_span)] = rsi_short
    df['rsi' + str(s.rsi_long_span)]  = rsi_long


    # ----------------------------
    # SMA
    # ----------------------------
    sma_short  = ta.SMA(
        close_data,
        timeperiod=s.sma_short_span
    )

    sma_middle = ta.SMA(
        close_data,
        timeperiod=s.sma_middle_span
    )

    sma_long = ta.SMA(
        close_data,
        timeperiod=s.sma_long_span
    )

    df['ma' + str(s.sma_short_span)]  = sma_short
    df['ma' + str(s.sma_middle_span)] = sma_middle
    df['ma' + str(s.sma_long_span)]   = sma_long


    # ----------------------------
    # Generate Cross Chart
    # ----------------------------
    sma_short    = df['ma' + str(s.sma_short_span)]
    sma_middle   = df['ma' + str(s.sma_middle_span)]
    cross  = sma_short > sma_middle

    cross_shift       = cross.shift(1)
    temp_golden_cross = (cross != cross_shift) & (cross == True)
    temp_dead_cross   = (cross != cross_shift) & (cross == False)

    golden_cross = [
        m if g == True else np.nan for g, m in zip(temp_golden_cross, sma_short)
    ]
    dead_cross   = [
        m if d == True else np.nan for d, m in zip(temp_dead_cross, sma_middle)
    ]

    df["gc"], df["dc"] = golden_cross, dead_cross

    pdf = df.tail(120)
    layout = {
                'title' : { 'text': f'{symbol}', 'x':0.5 },
                'xaxis' : { 'title': "Date", 'rangeslider': { 'visible': False } },
                'yaxis' : { 'title': "Price (JPY)", 'tickformat': ',' },
                'plot_bgcolor':'light blue'
    }

    data =  [
        pgo.Candlestick(
            name  = "chart",
            open  = pdf['Open'],
            high  = pdf['High'],
            low   = pdf['Low'],
            close = pdf['Close'],
            x     = pdf.index,
            increasing_line_color = '#00ada9',
            decreasing_line_color = '#a0a0a0'
        ),

        pgo.Scatter(
            name = 'MA' + str(s.sma_short_span),
            x    = pdf.index,
            y    = pdf["ma" + str(s.sma_short_span)],
            line = dict(
                color  = "#ff007f"
                ,width = 1.2
            )
        ),

        pgo.Scatter(
            name = 'MA' + str(s.sma_middle_span),
            x    = pdf.index,
            y    = pdf["ma" + str(s.sma_middle_span)],
            line = dict(
                color = '#7fbfff',
                width = 1.2
            )
        ),

        pgo.Scatter(
            name   = "Golden Cross",
            x      = pdf.index,
            y      = pdf["gc"],
            mode   = 'markers',
            marker = dict(
                size  = 12,
                color = 'blueviolet'
            )
        ),

        pgo.Scatter(
            name   = "Dead Cross",
            x      = pdf.index,
            y      = pdf["dc"],
            mode   = 'markers',
            marker = dict(
                size   = 12,
                color  ='black',
                symbol = 'x'
            )
        ),

        pgo.Scatter(
            name = '',
            x    = pdf.index,
            y    = pdf["bb_up"],
            line = dict(
                width = 0
            )
        ),

        pgo.Scatter(
            x    = pdf.index,
            y    = pdf["bb_low"],
            name = 'BB',
            fill ='tonexty',
            fillcolor = "rgba(170,170,170,0.25)",
            line = dict(
                width = 0
            )
        ),
    ]

    df.reset_index(inplace=True)

    days_list = [
        df.index[idx:idx + 3] for idx in range(0,len(df.index), 3)
    ]

    dates = [
        df['Date'][r[0]] for r in days_list
    ]

    fig = pgo.Figure(
        layout = pgo.Layout(layout),
        data = data
    )

    fig['layout'].update({
        'xaxis':{
            'showgrid': True,
            'tickvals': np.arange(0, df.index[-1],3),
            'ticktext': [x.strftime('%m/%d') for x in dates],
            }
    })

    pio.write_image(fig, image_name)
    print(f'Successfully generated image: {image_name}.')

def forecast_analysis_for_multi_symbols(symbols):
	for symbol in symbols:
		forecast_analysis(symbol)