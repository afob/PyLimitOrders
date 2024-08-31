from trading_framework.execution_client import (ExecutionClient,
                                                ExecutionException)
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []
        super().__init__()

    def add_order(self, product_id: str, amount: int, limit_price: float, buy: bool = False) -> None:
        """
        Adds a new limit order to the agent's list of orders.

        :param product_id: The product ID to buy or sell.
        :param amount: The number of shares to buy or sell.
        :param limit_price: The limit price at which to buy or sell.
        :param buy: A flag indicating whether the order is a buy (True) or sell (False). Default is False.
    """
        product_id = InputValue(product_id).validate_string(
            ValueError('product_id is empty.'))
        product_id = InputValue(product_id).validate_string(
            ValueError('product_id is empty.'))

        if amount <= 0:
            raise ValueError(
                'amount must be a positive integer greater than zero.')
        if limit_price <= 0:
            raise ValueError(
                'limit_price must be a positive number greater than zero.')
        
        self.orders.append({
            "product_id": product_id,
            "amount": amount,
            "limit_price": limit_price,
            "buy": buy,
        })

    def on_price_tick(self, product_id: str, price: float) -> None:
        """
            Handles price updates and executes orders if the market price meets the limit criteria.

            :param product_id: The ID of the product with a price change.
            :param price: The current market price of the product.
            """
         # Iterate over a copy of the list to avoid modifying it while iterating
        for order in list(self.orders):
            if order["product_id"] == product_id:
                if order["buy"] and price <= order["limit_price"]:
                    self._execute_order(order, price)
                elif not order["buy"] and price >= order["limit_price"]:
                    self._execute_order(order, price)

    def _execute_order(self, order: dict, price: float) -> None:
        """
        Executes an order and removes it from the list after execution.

        :param order: The order to be executed.
        :param price: The current market price.
        """
        try:
            if order["buy"]:
                self.execution_client.buy(order["product_id"], order["amount"])
                print(
                    f"Executed buy order for {order['amount']} shares of {order['product_id']} at price {price}")
            else:
                self.execution_client.sell(
                    order["product_id"], order["amount"])
                print(
                    f"Executed sell order for {order['amount']} shares of {order['product_id']} at price {price}")
            self.orders.remove(order)
        except ExecutionException as e:
            print(f"Failed to execute order: {e}")


class InputValue(object):
    def __init__(self, value):
        self.value = value

    def validate_string(self, exception,  default=None):
        """
        Validates and returns the string value or raises an exception if validation fails.

        :param exception: The exception to raise if validation fails.
        :param default: The default value to use if the initial value is empty.
        :return: The validated string.
        """
        if self.value:
            self.value = str(self.value)
        self.value = self.value.strip() if self.value else ''
        if not self.value:
            self.value = default.strip() if default is not None else ''
        if not self.value:
            raise exception
        return self.value