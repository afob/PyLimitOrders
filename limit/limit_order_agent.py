from trading_framework.execution_client import ExecutionClient, ExecutionException
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
        # # see PriceListener protocol and readme file
        # pass
         # Executing orders from an ExecutionClient instance
        self.execute_orders(product_id, price)

    def execute_orders(self, product_id: str, price: float):
        """executes orders on price tick"""
        executed_orders = []
        for order in self.orders:
            flag, order_product_id, amount, limit = order
            if product_id == order_product_id:
                print("executing order",order_product_id, amount)
                try:
                    if flag == 'buy' and price <= limit:
                        self.execution_client.buy(self,order_product_id, amount)
                        executed_orders.append(order)
                    elif flag == 'sell' and price >= limit:
                        self.execution_client.sell(self, order_product_id, amount)
                        executed_orders.append(order)
                        # Removing the executed sold order
                        self.orders.remove(order)
                    else:
                        raise ExecutionException
                except ExecutionException:
                    print(f"Something went wrong when executing an order")
        print("Executed Orders:",executed_orders)

    def add_order(self, flag: str, product_id: str, amount: int, limit: float):
        # Adding the bought order to orders list
        if flag not in ["buy","sell"]:
            raise ExecutionException
        self.orders.append((flag, product_id, amount, limit))
