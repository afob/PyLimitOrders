from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient):
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy, product_id, amount, limit):
        # Store order with details
        self.orders.append({
            'buy': buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })

    def price_tick(self, product_id, price):
        # Check each order to see if it should be executed
        for order in list(self.orders):
            if order['product_id'] == product_id:
                if (order['buy'] and price <= order['limit']) or (not order['buy'] and price >= order['limit']):
                    if order['buy']:
                        self.execution_client.execute_buy(order['product_id'], order['amount'])
                    else:
                        self.execution_client.execute_sell(order['product_id'], order['amount'])
                    self.orders.remove(order) 
