from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        self.execution_client = execution_client

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit_price: float):
        if is_buy:
            try:
                self.execution_client.buy(product_id, amount)
                print(f"Buy order for {amount} shares of {product_id} placed at limit price ${limit_price}.")
            except ExecutionException as e:
                print(f"Failed to place buy order: {e}")
        else:
            try:
                self.execution_client.sell(product_id, amount)
                print(f"Sell order for {amount} shares of {product_id} placed at limit price ${limit_price}.")
            except ExecutionException as e:
                print(f"Failed to place sell order: {e}")

    def on_price_tick(self, product_id: str, price: float):
        if product_id == "IBM" and price < 100:
            self.add_order(is_buy=True, product_id="IBM", amount=1000, limit_price=100)
