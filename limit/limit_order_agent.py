from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        Initialize the LimitOrderAgent with an execution client.

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []  # List to store all limit orders

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit_price: float) -> None:
        """
        Add a new limit order.

        :param is_buy: True for buy order, False for sell order.
        :param product_id: The ID of the product to trade.
        :param amount: The number of shares to trade.
        :param limit_price: The price limit for the order.
        """
        self.orders.append({
            'is_buy': is_buy,
            'product_id': product_id,
            'amount': amount,
            'limit_price': limit_price
        })

    def on_price_tick(self, product_id: str, price: float) -> None:
        """
        Called whenever a new market price is available.

        :param product_id: The ID of the product.
        :param price: The current market price.
        """
        # Check and execute orders that meet the limit price condition
        for order in self.orders[:]:  # Iterate over a copy of the list to safely remove items
            if order['product_id'] == product_id:
                if order['is_buy'] and price <= order['limit_price']:
                    self.execution_client.execute_order(product_id, order['amount'], 'buy')
                    self.orders.remove(order)
                elif not order['is_buy'] and price >= order['limit_price']:
                    self.execution_client.execute_order(product_id, order['amount'], 'sell')
                    self.orders.remove(order)
