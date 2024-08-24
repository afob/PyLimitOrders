from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit_price: float):
        """
        Adds a new limit order to the agent.

        :param is_buy: True if it's a buy order, False for a sell order.
        :param product_id: The ID of the product.
        :param amount: The amount to buy or sell.
        :param limit_price: The limit price for the order.
        """
        order = {
            "is_buy": is_buy,
            "product_id": product_id,
            "amount": amount,
            "limit_price": limit_price
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        """
        Called whenever there is a price update for a product.

        :param product_id: The ID of the product for which the price is updated.
        :param price: The updated price of the product.
        """
        # Iterate over a copy of the list to allow modification while iterating
        for order in list(self.orders):
            if order["product_id"] == product_id:
                if order["is_buy"] and price <= order["limit_price"]:
                    self.execution_client.buy(product_id, order["amount"])
                    self.orders.remove(order)
                elif not order["is_buy"] and price >= order["limit_price"]:
                    self.execution_client.sell(product_id, order["amount"])
                    self.orders.remove(order)
