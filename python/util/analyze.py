import stock.candle as cdl
import stock.sma as sma
import stock.bb as bb
import stock.macd as macd
import stock.rsi as rsi
import stock.multi_tech as multi_tech
import stock.sma_cross as sma_cross
import stock.forecast_analysis as forecast

# 単一銘柄で全テクニカル分析を実施
def all_analyze_for_only_symbol(symbol):
    """ Generate candle chart """
    cdl.candle(symbol)

    """ Generate SMA (simple moving average) chart """
    sma.sma(symbol)

    """ Generate BB (bollinger band) chart """
    bb.bb(symbol)

    """ Generate MACD (Moving Average Convergence Divergence) chart """
    macd.macd(symbol)

    """ Generate RSI (Relative Strength Index) chart """
    rsi.rsi(symbol)

    """ Generate multi tech chart (sma, macd, rsi) """
    multi_tech.multi_tech(symbol)

    """ Generate SMA cross chart """
    sma_cross.sma_cross(symbol)

    """ Generate forecast analysis chart """
    forecast.forecast_analysis(symbol)

# 複数銘柄で全テクニカル分析を実施
def all_analyze_for_multi_symbols(symbols):
    """ Generate candle chart for multi symbols """
    cdl.candle_for_multi_symbols(symbols)

    """ Generate SMA (simple moving average) chart for multi symbols """
    sma.sma_for_multi_symbols(symbols)

    """ Generate BB (bollinger band) chart for multi symbols """
    bb.bb_for_multi_symbols(symbols)

    """ Generate MACD (Moving Average Convergence Divergence) chart for multi symbols """
    macd.macd_for_multi_symbols(symbols)

    """ Generate RSI (Relative Strength Index) chart for multi symbols """
    rsi.rsi_for_multi_symbols(symbols)

    """ Generate multi tech chart (sma, macd, rsi) for multi symbols """
    multi_tech.multi_tech_for_multi_symbols(symbols)

    """ Generate SMA cross chart for multi symbols """
    sma_cross.sma_cross_for_multi_symbols(symbols)

    """ Generate forecast analysis chart for multi symbols """
    forecast.forecast_analysis_for_multi_symbols(symbols)


def to_be_analyze(symbols):
    multi_tech.multi_tech_for_multi_symbols(symbols)
    sma_cross.sma_cross_for_multi_symbols(symbols)
    forecast.forecast_analysis_for_multi_symbols(symbols)
