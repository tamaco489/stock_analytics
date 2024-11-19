import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate candle chart
def candle(symbol):
	image_name = f'./data/01_candle_chart_{symbol}.png'
	df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
	mpf.plot(df,
		type    = s.plot_type,
		volume  = s.is_volume,
		savefig = image_name
	)
	print(f'Successfully generated image: {image_name}.')

def candle_for_multi_symbols(symbols):
	for symbol in symbols:
		candle(symbol)