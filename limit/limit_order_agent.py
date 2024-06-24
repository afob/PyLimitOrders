from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.orders = []

    def add_order(self, buy_flag, product_id, amount, limit):
        order = {
            'buy_flag': buy_flag,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.orders:
            if (order['buy_flag'] and price < order['limit']):
                ExecutionClient.buy(self,order['product_id'],order['amount'])
            elif not order['buy_flag'] and price > order['limit']:
                ExecutionClient.sell(self,order['product_id'],order['amount'])

if __name__ == "__main__":

    try:

        # execution_client = MockExecutionClient()
        agent = LimitOrderAgent(PriceListener)

        # Add buy order for 1000 shares of IBM at $100 limit
        agent.add_order(True, 'IBM', 1000, 100)

        # Simulate price ticks
        agent.on_price_tick('IBM', 99)  # Order should not be executed
        agent.on_price_tick('IBM', 101)  # Order should be executed

        # Add sell order for 1000 shares of IBM at $150 limit
        agent.add_order(False, 'IBM', 1000, 150)

        # Simulate price ticks
        agent.on_price_tick('IBM', 160)  # Order should be executed

    except ExecutionException as e:
        print("An error occurred:", e)
