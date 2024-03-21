from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from limit_order_agent import LimitOrderAgent
from flag import FLAG

class Order(LimitOrderAgent):

    def place_order(self, product_id: str, price_limit: float, units: int, flag : FLAG):
        if units > 0 :
            LimitOrderAgent.add_order(product_id, price_limit, units*price_limit)
            return True
        return False