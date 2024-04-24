from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
import os
import sys

class LimitOrderAgent(PriceListener):
    product_id_price = {'ibm': 2000, 'cts': 3000, 'tata': 900, 'hdfc': 800}
    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy_order: bool, product_id: str, amount: int, limit_price: float):
        #Add to orders list with relevant data
        if buy_order is True:
            buy_type = 'buy'
        else:
            buy_type = 'sell'
        self.orders.append({
            'type': buy_type,
            'product_id': product_id,
            'amount': amount,
            'limit': limit_price
        })


    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.orders:
            if order['product_id'] == product_id:
                try:
                    if str(order['type']).lower() == 'buy' and price <= order['limit_price']:
                        self.execution_client.buy(product_id, order['amount'])
                        self.orders.remove(order)
                    elif str(order['type']).lower() == 'sell' and price >= order['limit_price']:
                        self.execution_client.sell(product_id, order['amount'])
                        self.orders.remove(order)
                except Exception as e:
                    print(f"Failed to execute order: {e}")




