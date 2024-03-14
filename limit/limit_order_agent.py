from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

BUY = True
SELL = False

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders={}
        self.completed_orders = {}

    def on_price_tick(self, product_id: str, price: float):

        """
        Executed on price change for each product
        :param product_id: the product Id
        :param price: price of the product
        :return: returns none
        """
        #if product_id == 'IBM' and float(price) <= float(100):
        #    self.run_orders(product_id, price)
        self.run_orders(product_id, price)

    def add_order(self, operation:bool, product_id: str, amount: int, limit: float):
        order = {
            'limit': limit,
            'amount': amount,
            'operation': operation
        }

        if product_id in self.orders.keys():
            self.execution_client.buy(product_id, 100)
        else:
            self.orders[product_id] = [order]


    def run_orders(self, product_id: str, price: float):
        operation_completed = None

        if product_id in self.orders.keys():
            for order in self.orders[product_id]:
                if order['operation'] == BUY and float(price) <= float(order['limit']):
                    self.execution_client.buy(product_id, order['amount'])
                    operation_completed = 'buy'


                elif order['operation'] == SELL and float(price) >= float(order['limit']):
                    self.execution_client.sell(product_id, order['amount'])
                    operation_completed = 'sell'


                if operation_completed:
                    print('Executed Client to {} {} units of {} at price {}' \
                         .format(operation_completed, str(order['amount']), product_id, str(price)))

                    self.orders[product_id].remove(order)
                    if product_id in self.completed_orders.keys():
                        self.completed_orders[product_id].append(order)
                    else:
                        self.completed_orders[product_id] = [order]
        else:
            print('No orders to run for {}'.format(product_id))



