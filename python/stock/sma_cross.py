import talib as ta
import pandas_datareader.data as pdr
import plotly.graph_objs as pgo
import plotly.io as pio
import numpy as np
import vars.stock as s

# Generate SMA cross chart
def sma_cross(symbol):
    image_name = f'./data/07_sma_cross_chart_{symbol}.png'
    df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
    close = df['Close']                               # 終値を使用してSMA算出

    # SMA: main.pyで短期EMAを5日, 長期EMAを25日に指定
    short_span, middle_span = ta.SMA(close, timeperiod=s.sma_short_span), ta.SMA(close, timeperiod=s.sma_middle_span)
    df['ma' + str(s.sma_short_span)], df['ma' + str(s.sma_middle_span)] = short_span, middle_span

    # 短期EMAが長期EMAを上回っている場合はTrue
    cross = short_span > middle_span

    # ゴールデンクロス, デッドクロス発生日検知フラグ検カラム定義
    cross_shift = cross.shift(1)
    temp_golden_cross = (cross != cross_shift) & (cross == True)
    temp_dead_cross   = (cross != cross_shift) & (cross == False)

    # ゴールデンクロスとデッドクロスのカラム定義
    golden_cross = [m if g == True else np.nan for g, m in zip(temp_golden_cross, short_span)]
    dead_cross   = [m if d == True else np.nan for d, m in zip(temp_dead_cross, middle_span)]
    df["gc"], df["dc"] = golden_cross, dead_cross

    # 直近200日分のデータを指定
    df = df.tail(200)

    # グラフレイアウト指定
    layout = {
        'title'  : { 'text': f'{symbol}', 'x':0.5 },
        'xaxis' : { 'title': "Date", 'rangeslider': { 'visible': False } },
        'yaxis' : { 'title': "Price (JPY)", 'side': "left", 'tickformat': ',' },
        'plot_bgcolor':'light blue'
    }

    data = [
        pgo.Candlestick(
            name  = 'chart',
            open  = df['Open'],
            high  = df['High'],
            low   = df['Low'],
            close = df['Close'],
            x     = df.index,
            increasing_line_color = '#00ada9',
            decreasing_line_color = '#a0a0a0'
        ),

        pgo.Scatter(
            name = 'MA' + str(s.sma_short_span),
            x    = df.index,
            y    = df["ma" + str(s.sma_short_span)],
            line = dict(
                color = "#ff007f",
                width = 1.2
            )
        ),

        pgo.Scatter(
            name = 'MA' + str(s.sma_middle_span),
            x    = df.index,
            y    = df["ma" + str(s.sma_middle_span)],
            line = dict(
                color = '#7fbfff',
                width = 1.2
            )
        ),

        pgo.Scatter(
            name   = "Golden Cross",
            mode   = 'markers',
            x      = df.index,
            y      = df["gc"],
            marker = dict(
                size  = 12,
                color = 'blueviolet'
            )
        ),

        pgo.Scatter(
            name   = "Dead Cross",
            mode   = 'markers',
            x      = df.index,
            y      = df["dc"],
            marker = dict(
                size   = 12,
                color  = 'black',
                symbol = 'x'
            )
        )
    ]

    fig = pgo.Figure(
        layout = pgo.Layout(layout),
        data = data
    )

    file_name = image_name
    pio.write_image(fig, f"{file_name}.png")
    print(f'Successfully generated image: {image_name}.')

def sma_cross_for_multi_symbols(symbols):
	for symbol in symbols:
		sma_cross(symbol)