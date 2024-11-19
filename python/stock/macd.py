import talib as ta
import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate MACD (Moving Average Convergence Divergence) chart
def macd(symbol):
    image_name = f'./data/04_macd_chart_{symbol}.png'
    df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
    data = df['Close']                          # 終値を使用してMACDで計算

    macd, macdsignal, _ = ta.MACD(data,
                                fastperiod   = s.macd_short_span,  # 短期EMA
                                slowperiod   = s.macd_long_span,   # 長期EMA
                                signalperiod = s.macd_signal       # 売買シグナル
                            )
    df['macd'] = macd
    df['macd_signal'] = macdsignal

    mdf = df.tail(100)                          # 直近100日分のデータを指定

    apd  = [
        mpf.make_addplot(mdf['macd'], panel=2, color='red'),         # パネルの2番地に赤で描画
        mpf.make_addplot(mdf['macd_signal'], panel=2, color='blue'),
    ]

    mpf.plot(mdf,
            type    = s.plot_type,
            addplot = apd,
            volume  = s.is_volume,
            savefig = image_name
    )
    print(f'Successfully generated image: {image_name}.')

def macd_for_multi_symbols(symbols):
    for symbol in symbols:
        macd(symbol)