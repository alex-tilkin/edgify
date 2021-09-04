from order import Order
from trading_source import TradingSource
import pandas as pd


class TradingCsv(TradingSource):
    def __init__(self):
        super(TradingCsv, self).__init__()
        self.ID = 'Id'
        self.Type = 'Type'
        self.PRICE = 'Price'
        self.AMOUNT = 'Amount'
        self.col_names = [self.ID, self.Type, self.PRICE, self.AMOUNT]

    def to_memory(self, file_path):
        super(TradingCsv, self).to_memory()
        self.csv_data = pd.read_csv(file_path, names=self.col_names, header=0)

        for i, csv_item in self.csv_data.iterrows():
            order = Order(csv_item[self.ID], csv_item[self.Type], csv_item[self.PRICE], csv_item[self.AMOUNT])
            self.orders.append(order)
