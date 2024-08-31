class ExecutionClient:
    def execute_order(self, product_id: str, amount: int, order_type: str) -> None:
        """
        Mock execute_order method for testing.

        :param product_id: The ID of the product to buy/sell.
        :param amount: The number of shares to buy/sell.
        :param order_type: 'buy' or 'sell'.
        """
        print(f"Executing {order_type} order for {amount} shares of {product_id}.")
