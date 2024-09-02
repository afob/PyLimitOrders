from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []
    
    def add_order(self, is_buy, product_id, amount, limit):
        order = {
            'is_buy': is_buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        executed_orders = []
        for order in self.orders:
            if order['product_id'] == product_id:
                if (order['is_buy'] and price <= order['limit']) or (not order['is_buy'] and price >= order['limit']):
                    if order['is_buy']:
                        self.execution_client.buy(order['product_id'], order['amount'])
                    else:
                        self.execution_client.sell(order['product_id'], order['amount'])
                    executed_orders.append(order)

        # Remove executed orders from the list
        for order in executed_orders:
            self.orders.remove(order)
