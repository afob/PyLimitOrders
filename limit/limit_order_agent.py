from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        Initialize the LimitOrderAgent with an execution client.
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        """
        Callback function invoked on market data change.
        :param product_id: ID of the product that has a price change.
        :param price: The current market price of the product.
        """
        if product_id == 'IBM' and price < 100:
            self.execute_order('buy', 'IBM', 1000, price)

    def add_order(self, action: str, product_id: str, amount: int, limit_price: float):
        """
        Add an order to the agent's queue.
        :param action: 'buy' or 'sell'.
        :param product_id: The ID of the product.
        :param amount: The amount to buy or sell.
        :param limit_price: The limit price for the order.
        """
        self.orders.append((action, product_id, amount, limit_price))

    def execute_order(self, action: str, product_id: str, amount: int, price: float):
        """
        Execute orders when the market price is at or better than the limit.
        :param action: 'buy' or 'sell'.
        :param product_id: The ID of the product.
        :param amount: The amount to buy or sell.
        :param price: The current market price.
        """
        for order in self.orders[:]:  # Iterate over a copy of the list
            if order[0] == action and order[1] == product_id and price >= order[3]:
                try:
                    if action == 'buy':
                        self.execution_client.buy(product_id, amount)
                    else:
                        self.execution_client.sell(product_id, amount)
                    print(f"Executed {action} order for {amount} {product_id} at price {price}")
                    self.orders.remove(order)
                except ExecutionException as e:
                    print(f"Execution failed: {e}")

