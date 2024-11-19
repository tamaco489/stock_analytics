import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate SMA (simple moving average) chart
def sma(symbol):
	image_name = f'./data/02_candle_sma_chart_{symbol}.png'
	df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
	mpf.plot(df,
		type    = s.plot_type,
		mav     = (s.sma_short_span, s.sma_middle_span, s.sma_long_span),
		volume  = s.is_volume,
		savefig = image_name
	)
	print(f'Successfully generated image: {image_name}.')

def sma_for_multi_symbols(symbols):
	for symbol in symbols:
		sma(symbol)