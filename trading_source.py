
class TradingSource():
    def __init__(self):
        self.orders = []

    def to_memory(self):
        self.orders = []

    def get_orders(self):
        """
        :type listOfOrders: list<Order>
        """
        return self.orders
