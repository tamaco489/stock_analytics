import talib as ta
import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate RSI (Relative Strength Index) chart
def rsi(symbol):
    image_name = f'./data/05_rsi_chart_{symbol}.png'
    df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
    data = df['Close']                               # 終値を使用してRSIで計算

    rsi_short = ta.RSI(data, timeperiod=s.rsi_short_span)          # 短期EMA
    rsi_long  = ta.RSI(data, timeperiod=s.rsi_long_span)           # 長期EMA
    df['rsi' + str(s.rsi_short_span)], df['rsi' + str(s.rsi_long_span)] = rsi_short, rsi_long   # 指定期間をDataFrameに設定

    mdf = df.tail(100)                               # 直近100日分のデータを指定

    apd  = [
        mpf.make_addplot(mdf['rsi' + str(s.rsi_short_span)], panel=2, color='red'),
        mpf.make_addplot(mdf['rsi' + str(s.rsi_long_span)],  panel=2, color='blue')
    ]

    mpf.plot(mdf,
            type    = s.plot_type,
            addplot = apd,
            volume  = s.is_volume,
            savefig = image_name
    )
    print(f'Successfully generated image: {image_name}.')

def rsi_for_multi_symbols(symbols):
    for symbol in symbols:
        rsi(symbol)