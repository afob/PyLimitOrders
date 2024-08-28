from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = ExecutionClient
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.orders:
            if order['product_id'] == product_id:
                try:
                    if order['type'] == 'buy' and price <= order['price_limit']:
                        self.execution_client.buy(product_id, order['price'])
                        self.orders.remove(order)
                    elif order['type'] == 'sell' and price >= order['price_limit']:
                        self.execution_client.sell(product_id, order['price'])
                        self.orders.remove(order)
                except Exception as e:
                    print(f"Failed to execute order: {e}")

    def add_order(self,order_type: str,product_id: str, price: float,price_limit: float):
        self.orders.append({
            'type': order_type,
            'product_id': product_id,
            'price': price,
            'price_limit': price_limit
        })

