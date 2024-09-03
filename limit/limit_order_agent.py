from trading_framework import ExecutionClient

class LimitOrderAgent:
    def __init__(self, execution_client: ExecutionClient):
        """
        Initialize the LimitOrderAgent with an execution client and an empty list of orders.
        
        :param execution_client: The client used to execute orders.
        """
        self.execution_client = execution_client
        self.orders = []

    def price_tick(self, product_id: str, price: float):
        """
        Called whenever there is a new market price. Checks all orders and executes
        any that meet the criteria.

        :param product_id: The ID of the product for which the price is provided.
        :param price: The current market price of the product.
        """
        for order in self.orders[:]:  # Create a copy of the list for safe iteration
            if order['product_id'] == product_id:
                if order['buy'] and price <= order['limit']:
                    self.execution_client.execute_order(product_id, order['amount'], 'buy')
                    self.orders.remove(order)
                elif not order['buy'] and price >= order['limit']:
                    self.execution_client.execute_order(product_id, order['amount'], 'sell')
                    self.orders.remove(order)

    def add_order(self, buy: bool, product_id: str, amount: int, limit: float):
        """
        Add a new limit order to the agent.

        :param buy: True if the order is to buy, False if it's to sell.
        :param product_id: The ID of the product to buy/sell.
        :param amount: The number of shares to buy/sell.
        :param limit: The limit price for buying/selling.
        """
        order = {
            'buy': buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)
