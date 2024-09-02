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

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if product_id == "IBM" and price < 100:
            try:
                self.execution_client.buy(product_id, 1000)
            except Exception as e:
                print(f"Failed to execute buy order: {e}")


    def add_order(self, buy: bool, product_id: str, amount: int, limit_price: float):
        self.orders.append({
            "buy": buy,
            "product_id": product_id,
            "amount": amount,
            "limit_price": limit_price
        })

    def process_orders(self):
        for order in self.orders:
            if order["buy"]:
                if self.current_price <= order["limit_price"]:
                    try:
                        self.execution_client.buy(order["product_id"], order["amount"])
                        self.orders.remove(order)
                    except Exception as e:
                        print(f"Failed to execute buy order: {e}")
            else:
                if self.current_price >= order["limit_price"]:
                    try:
                        self.execution_client.sell(order["product_id"], order["amount"])
                        self.orders.remove(order)
                    except Exception as e:
                        print(f"Failed to execute sell order: {e}")
