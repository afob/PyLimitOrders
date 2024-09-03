
from trading_framework.execution_client import ConcreteExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ConcreteExecutionClient) -> None:
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        self.orders.append((action, product_id, amount, limit))

    def on_price_tick(self, product_id: str, price: float):
        to_execute = [order for order in self.orders if order[1] == product_id and 
                      ((order[0] == 'buy' and price < order[3]) or 
                       (order[0] == 'sell' and price > order[3]))]
        
        for action, product_id, amount, limit in to_execute:
            if action == 'buy':
                self.execution_client.buy(product_id, amount)
            elif action == 'sell':
                self.execution_client.sell(product_id, amount)
            self.orders.remove((action, product_id, amount, limit))

