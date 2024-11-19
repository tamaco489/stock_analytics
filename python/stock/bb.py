from pyti.bollinger_bands import upper_bollinger_band as bb_up
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from pyti.bollinger_bands import lower_bollinger_band as bb_low
import mplfinance as mpf
import pandas_datareader.data as pdr
import vars.stock as s

# Generate BB (bollinger band) chart
def bb(symbol):
	image_name = f'./data/03_bb_chart_{symbol}.png'
	df = pdr.DataReader(symbol, s.finance, s.start, s.end).sort_index()
	data = df['Close'].tolist()        # 終値をリスト型に変換

	period = s.sma_middle_span         # 中期移動平均線をmiddle_bandとする
	upper_band  = bb_up(data, period)
	middle_band = bb_mid(data, period)
	lower_band  = bb_low(data, period)

	df['bb_up']  = upper_band
	df['bb_mid'] = middle_band
	df['bb_low'] = lower_band

	apd = mpf.make_addplot(df[['bb_up', 'bb_mid', 'bb_low']])
	mpf.plot(df,
			type    = s.plot_type,
			addplot = apd,
			volume  = s.is_volume,
			savefig = image_name
	)
	print(f'Successfully generated image: {image_name}.')

def bb_for_multi_symbols(symbols):
	for symbol in symbols:
		bb(symbol)