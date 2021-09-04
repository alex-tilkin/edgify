from flask import Response

from files_storage import FilesStorage
from trading_source import TradingSource
from transactions_calculator import TransactionsCalculator


class TradeService:
    def __init__(self, files_storage: FilesStorage, trading_source: TradingSource,
                 transactions_calculator: TransactionsCalculator):
        self.files_storage = files_storage
        self.trading_source = trading_source
        self.transactions_calculator = transactions_calculator

    def trade(self, request):
        status = self.__validate_attachment(request)
        if status is not None:
            return status

        uploaded_file = request.files['file']
        file_path = self.files_storage.save(uploaded_file)
        self.trading_source.to_memory(file_path)
        return self.transactions_calculator.calculate(self.trading_source)

    def __validate_attachment(self, request):
        if 'file' not in request.files or request.files['file'] == '':
            return Response(
                "Missing trading file",
                status=400,
            )

        return None
