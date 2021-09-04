import json

import exchange_rates
from trading_source import TradingSource


class TransactionsCalculator:
    def __init__(self, exchange_rates: exchange_rates):
        self.exchange_rates = exchange_rates

    def calculate(self, trading_source: TradingSource):
        orders = trading_source.get_orders()

        buy_orders = [order for order in orders if order.type == 'Buy' and order.price != 'Market']
        sell_orders = [order for order in orders if order.type == 'Sell' and order.price != 'Market']
        market_orders = [order for order in orders if order.price == 'Market']

        data = {}
        for buy_order in buy_orders:
            usd_price = self.exchange_rates.fetch_latest_eur_usd_rate()
            if float(buy_order.price) > usd_price:
                data[buy_order.id] = self.__create_executed_order(buy_order, usd_price)
            else:
                data[buy_order.id] = self.__create_denied_order()

        for sell_order in sell_orders:
            usd_price = self.exchange_rates.fetch_latest_eur_usd_rate()
            if float(sell_order.price) < usd_price:
                data[sell_order.id] = self.__create_executed_order(sell_order, usd_price)
            else:
                data[sell_order.id] = self.__create_denied_order()

        for market_order in market_orders:
            total_amount = market_order.amount
            stored_items = []
            stored_amounts = {}
            for item in data.items():
                value = item[1]['amount']
                if total_amount > value:
                    total_amount = total_amount - value
                    stored_amounts[item[0]] = value
                else:
                    stored_amounts[item[0]] = total_amount
                    total_amount = 0

                stored_items.append(item)
                if total_amount == 0:
                    break

            weighted_average, sum = self.__calculate_weighted_average_and_sum(data, stored_amounts)

            data[market_order.id] = self.__create_market_order(weighted_average, stored_items, stored_amounts, sum)

        return json.dumps(data, indent=4, sort_keys=True)

    def __calculate_weighted_average_and_sum(self, data, stored_amounts):
        weighted_sum = 0
        sum = 0
        for stored_amount in stored_amounts.items():
            weighted_sum = weighted_sum + stored_amount[1] * data[stored_amount[0]]['price']
            sum = sum + stored_amount[1]

        weighted_average = weighted_sum / sum

        return weighted_average, sum

    def __create_market_order(self, weighted_average, stored_items, stored_amounts, amount):
        return {
            'status': "Executed",
            'price': weighted_average,
            'amount': amount,
            'total': amount * weighted_average,
            'orders': stored_amounts
        }

    def __create_executed_order(self, order, usd_price):
        return {
            'status': "Executed",
            'amount': order.amount,
            'price': usd_price,
            'total': order.amount * usd_price
        }

    def __create_denied_order(self):
        return {
            'status': "Denied"
        }
