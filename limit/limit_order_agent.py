from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient):
        self.execution_client = execution_client
        self.orders = []  # Stores orders as tuples: (side, product_id, amount, limit_price)

    def add_order(self, side: str, product_id: str, amount: int, limit_price: float):
        """Add an order to the list of orders."""
        if side not in {'buy', 'sell'}:
            raise ValueError("Order side must be 'buy' or 'sell'.")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if limit_price <= 0:
            raise ValueError("Limit price must be greater than 0.")
        
        self.orders.append((side, product_id, amount, limit_price))


    def on_price_tick(self, product_id: str, price: float):
        """Process the incoming market data and execute orders if conditions are met."""
        orders_to_remove = []
        for order in self.orders:
            side, pid, amount, limit_price = order
            if pid == product_id:
                try:
                    if side == 'buy' and price <= limit_price:
                        self.execution_client.buy(product_id, amount)
                        orders_to_remove.append(order)
                    elif side == 'sell' and price >= limit_price:
                        self.execution_client.sell(product_id, amount)
                        orders_to_remove.append(order)
                except ExecutionException:
                    print(f"Failed to execute {side} order for {product_id} due to execution error.")
                    # Handle execution failure

        # Remove executed orders after processing
        for order in orders_to_remove:
            self.orders.remove(order)
