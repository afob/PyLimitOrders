import random

from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
import logging


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.held_orders = []

    def on_price_tick(self, product_id: str, price: float):
        current_share_price = random.random.uniform(price - 2, price + 2) # We can add live price scraper here
        return product_id,current_share_price

    def add_order(self, product_id,amount,limit,action):
        """
        Add an order to the list of held orders.
        """
        if action not in ["BUY","SELL"]:
            raise Exception ("Action Should be BUY or SELL")
        order = {'product_id': product_id, 'amount': amount, 'limit': limit,'action': action}
        self.held_orders.append(order)

    def execute_held_orders(self):
        while self.held_orders:
            executed_orders=[]
            if self.held_orders:
                for order in self.held_orders:
                    try:
                        product_id,current_share_price = self.on_price_tick(order['product_id'], order['limit'])
                        if current_share_price:
                            if order["action"] == "BUY" and order["limit"] >= current_share_price and order['product_id']==product_id:
                                self.execution_client.buy(order['product_id'], order['amount'])
                                executed_orders.append(order)

                            elif order["action"] == "SELL" and order["limit"] <= current_share_price and order['product_id']==product_id:
                                self.execution_client.sell(order['product_id'], order['amount'])
                                executed_orders.append(order)

                    except Exception as e:
                        logging.warning('execution failed due to : {}'.format(e))
                        # If execution fails, remove the order from executed_orders
                        executed_orders.remove(order)
            # Remove executed orders from held_orders
            for order in executed_orders:
                self.held_orders.remove(order)


