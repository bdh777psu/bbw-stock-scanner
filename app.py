from flask import Flask, render_template, request
import tradingview_ta as tv_ta
from binance.spot import Spot as Client
import os


app = Flask(__name__)

client = Client()

symbols_dir = 'exchanges/'
exchanges = ["NYSE", "NASDAQ", "BMFBOVESPA", "BINANCE"]
intervals = ["5m" ,"15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"]

filtered_symbols = {}


@app.route('/', methods=['GET'])
def load():
    """Returns the rendered starting page with default values"""
    filtered_symbols.clear()
    
    return render_template('index.html', exchanges=exchanges, stock_symbols=filtered_symbols, intervals=intervals)


@app.route('/', methods=['POST'])
def scan():
    """Exibits the Bollinger Bands width, price and % change in price for multiple stocks at once"""
    filtered_symbols.clear()

    input_interval = request.form.get("intervals")
    input_bbw = request.form.get("bbw")
    input_exchange = request.form.get("exchanges")

    available_symbols = open_file(input_exchange)

    analysis = symbol_analysis(input_exchange, input_interval, available_symbols)

    calculate_bbw(analysis, input_bbw)
    calculate_current_price(analysis)
    calculate_price_change(analysis)
    recommend_symbols(analysis)

    return render_template('index.html', exchanges=exchanges, stock_symbols=filtered_symbols, intervals=intervals)


def open_file(exchange):
    """Returns the ticker symbols available for the chosen exchange"""
    if exchange != "BINANCE":
        exchange_file = symbols_dir + exchange + ".txt"

        try:
            with open(exchange_file) as file:
                stock_symbols = file.read()
                file.close
                    
                return stock_symbols.split('\n')
        except:
            print("Something went wrong: Unable to read file!")
    else:
        exchange_info = client.exchange_info()
        exchange_pairs = set()
        pairs = str()

        for s in exchange_info['symbols']:
            if s['symbol'].endswith('USDT'):
                exchange_pairs.add('BINANCE:' + s['symbol'])
        
        for pair in exchange_pairs:
            pairs += pair + '\n'

        return pairs[:-1].split('\n')

def symbol_analysis(exchange, interval, symbols):
    """Returns a dictionary of a TradingView analysis of multiple stocks at once"""
    match exchange:
        case "NYSE":
            screener = "america"
        case "NASDAQ":
            screener = "america"
        case "BMFBOVESPA":
            screener = "brazil"
        case "BINANCE":
            screener = "crypto"

    return tv_ta.get_multiple_analysis(screener=screener, interval=interval, symbols=symbols)


def calculate_bbw(analysis_dict, input_bbw):
    """Calculates the Bollinger Bands width for multiple stocks at once"""
    for symbol, value in analysis_dict.items():
        try:
            if symbol or value is not None:
                upper = value.indicators["BB.upper"]
                lower = value.indicators["BB.lower"]
                sma = value.indicators["SMA20"]

                bbw = (upper - lower) / sma

                if bbw < 1 and bbw < float(input_bbw):
                    bbw = round(bbw, 4)
                    filtered_symbols[symbol] = [bbw]
        except TypeError:
            print(symbol, "is not defined!")
        except AttributeError:
            print(symbol, "is missing bbw calculation values!")
        except ZeroDivisionError:
            print(symbol, "bbw division by SMA zero value!")     


def calculate_current_price(analysis_dict):
    """Calculates the Closing price for multiple stocks at once"""
    for symbol, value in analysis_dict.items():
        try:
            if symbol in filtered_symbols.keys():
                close = value.indicators["close"]
                closing_price = round(close, 2)
                
                filtered_symbols[symbol].append(closing_price)
        except AttributeError:
            print(symbol, "is missing Closing price info!")
        except KeyError:
            print(symbol, "is not defined!")


def calculate_price_change(analysis_dict):
    """Calculates the percent change in price for multiple stocks at once"""
    for symbol, value in analysis_dict.items():
        try:
            if symbol in filtered_symbols.keys():
                open = value.indicators["open"]
                close = value.indicators["close"]

                price_change = ((close - open) / open) * 100
                price_change = round(price_change, 2)
                            
                filtered_symbols[symbol].append(price_change)
        except AttributeError:
            print(symbol, "is missing Opening or Closing price info!")
        except KeyError:
            print(symbol, "is not defined!")
        except ZeroDivisionError:
            print(symbol, "Opening price set to zero value!")


def recommend_symbols(analysis_dict) -> int:
    """Filters for recomendations"""        
    for symbol, value in analysis_dict.items():

        try:
            recommendation = value.summary["RECOMMENDATION"]
        
            filtered_symbols[symbol].append(recommendation.replace('_', ' '))
        except AttributeError:
            print(symbol, "does not have associated recommendation!")
        except KeyError:
            print(symbol, "is not defined!")


@app.errorhandler(404)
def pageNotFound(error):
    """Exibits the '404 error' page"""
    return render_template('error.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))