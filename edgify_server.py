from flask import Flask, render_template, request

from exchange_rates import ExchangeRates
from files_storage import FilesStorage
from trade_service import TradeService
from trading_csv import TradingCsv
from transactions_calculator import TransactionsCalculator

app = Flask(__name__)

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


@app.route('/api/trade', methods=['POST'])
def trade():
    return trade_service.trade(request)


if __name__ == "__main__":
    upload_folder = ''
    files_storage = FilesStorage(upload_folder)
    trading_source = TradingCsv()
    exchange_rates = ExchangeRates()
    transactions_calculator = TransactionsCalculator(exchange_rates)
    trade_service = TradeService(files_storage, trading_source, transactions_calculator)

    app.config["DEBUG"] = True
    app.run(port=5000)
