from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        self.execution_client = execution_client
        self.orders = [] # Queue for storing orders.
    def add_order(self,type, pid, amt, limit):
        """
        Add the order in the queue to execute it on the basis of triggers.
        """
        if type not in {'buy', 'sell'}:
            raise ValueError("Type for the order must be either 'buy' or 'sell'.")
        if amt <= 0:
            raise ValueError("Amount must be greater than 0.")
        if limit <= 0:
            raise ValueError("Limit should be greater than 0.") 
        self.orders.append({'type':type, 'pid':pid, 'amt':amt, 'limit':limit})
        print(f"Order {(type, pid, amt, limit)} Added Successfully.")

        
    def on_price_tick(self, product_id: str, price: float):
        """
        execute the orders in the queue for based on the type and limits.
        """
        completed_order = []
        for order in self.orders:
            if order['pid'] == product_id:
                try:
                    if order['type'] == 'buy' and order['limit'] >= price:
                        self.execution_client.buy(product_id, order['amt'])
                        completed_order.append(order)
                    if order['type'] == 'sell' and order['limit'] <= price:
                        self.execution_client.sell(product_id, order['amt'])
                        completed_order.append(order)
                except Exception as e:
                    raise ExecutionException(f"Failed to execute {order['type']} order for {order['pid']}.")
                
                for order in completed_order:
                    self.orders.remove(order) # Removing the orders from the queue after successfully execution.
                
            


                
