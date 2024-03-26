from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from limit_order_agent import LimitOrderAgent
from flag import FLAG

class Order(LimitOrderAgent):

    # product_details = [{product_id: str, price_limit: float, units: int, flag :FLAG},{product_id: str, price_limit: float, units: int, flag :FLAG}]
    def place_order(self, product_details:list):
        for product_detail in product_details:
            if product_detail['units'] > 0 :
                LimitOrderAgent.add_order(product_detail['flag'],product_detail['product_id'], product_detail['price_limit'], product_detail['units']*product_detail['price_limit'])
        return True    

