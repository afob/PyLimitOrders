from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from limit_order_agent import LimitOrderAgent


class Order(LimitOrderAgent):

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if product_id == 'IBM' and price < 100:
            LimitOrderAgent.add_order('buy', product_id, price, 1000*price)
            return True
