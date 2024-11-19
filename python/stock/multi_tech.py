import talib as ta
import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate multi tech chart (sma, macd, rsi)
def multi_tech(symbol):
    image_name = f'./data/06_multi_tech_{symbol}.png'
    df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
    data = df['Close']                               # 終値を使用してRSIで計算

    # sma initialize
    sma_short, sma_middle, sma_long  = ta.SMA(data, timeperiod=s.sma_short_span), ta.SMA(data, timeperiod=s.sma_middle_span), ta.SMA(data, timeperiod=s.sma_long_span)
    df['ma' + str(s.sma_short_span)], df['ma' + str(s.sma_middle_span)], df['ma' + str(s.sma_long_span)] = sma_short, sma_middle, sma_long

    # macd initialize
    macd, macdsignal, _ = ta.MACD(data, fastperiod=s.macd_short_span, slowperiod=s.macd_long_span, signalperiod=s.macd_signal)
    df['macd'], df['macd_signal'] = macd, macdsignal

    # rsi initialize
    rsi_short, rsi_long = ta.RSI(data, timeperiod=s.rsi_short_span), ta.RSI(data, timeperiod=s.rsi_long_span)
    df['rsi' + str(s.rsi_short_span)], df['rsi' + str(s.rsi_long_span)] = rsi_short, rsi_long

    mdf = df.tail(200)                               # 直近200日分のデータを指定

    apd  = [
        mpf.make_addplot(mdf['ma' + str(s.sma_short_span)],  panel=0, color='blue'),
        mpf.make_addplot(mdf['ma' + str(s.sma_middle_span)], panel=0, color='purple'),
        mpf.make_addplot(mdf['ma' + str(s.sma_long_span)],   panel=0, color='yellow'),

        mpf.make_addplot(mdf['macd'],        panel=2, color='red'),
        mpf.make_addplot(mdf['macd_signal'], panel=2, color='blue'),

        mpf.make_addplot(mdf['rsi' + str(s.rsi_short_span)], panel=3, color='red'),
        mpf.make_addplot(mdf['rsi' + str(s.rsi_long_span)],  panel=3, color='blue')
    ]

    mpf.plot(mdf,
            type    = s.plot_type,
            addplot = apd,
            volume  = s.is_volume,
            savefig = image_name
    )
    print(f'Successfully generated image: {image_name}.')

def multi_tech_for_multi_symbols(symbols):
    for symbol in symbols:
        multi_tech(symbol)
