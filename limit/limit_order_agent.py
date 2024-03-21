from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.held_orders = []

    def on_price_tick(self, product_id: str, price: float):
        if product_id == 'IBM' and price < 100:
            self.execution_client.buy('IBM', 1000)
        self.execute_held_orders(product_id, price)

    def add_order(self, buy_flag: bool, product_id: str, amount: int, limit: float):
        """
        Add an order to the list of held orders.
        """
        self.held_orders.append((buy_flag, product_id, amount, limit))

    def execute_held_orders(self, product_id: str, current_price: float):
        executed_orders = []
        for buy_flag, product, amount, limit in self.held_orders:
            if product == product_id and buy_flag and current_price <= limit:
                self.execution_client.buy(product_id, amount, limit)
                executed_orders.append((buy_flag, product_id, amount, limit))
            if product == product_id and not buy_flag and current_price >= limit:
                self.execution_client.sell(product_id, amount, limit)
                executed_orders.append((buy_flag, product_id, amount, limit))
        for order in executed_orders:
            self.held_orders.remove(order)

