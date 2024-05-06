from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.orders = []  
        super().__init__()

    def add_order(self, order_type: str, product_id: str, price: float, limit: int):
        if order_type == "BUY" or order_type == "SELL":
            self.orders.append({'flag' : order_type , 'Product_id':product_id , 'amount':price , 'limit' : limit, 'order_completed': False})

    def execute_order(self, product_id: str, price: float):
        for order in self.orders:
            if product_id == order['Product_id']:
                if price < order['limit'] and order['flag']=="BUY":
                    if order['order_completed'] != True:
                        self.execution_client.buy(product_id , order['amount']) 
                        order['order_completed'] = True
                    else:
                        print("Order already place")
                elif self.market_price >= order.amount and order.flag=="SELL":
                    if order['order_completed'] != True:
                        self.execution_client.sell(product_id , order['amount']) 
                        order['order_completed'] = True
                    else:
                        print("Order already place")
                else:
                    print("Can't place order")
            else:
                print("Product Id does not exist")
        # reomve completed orders from add orders list
        self.orders = list(filter(lambda o: o['order_completed'] != True, self.orders))

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        #pass
        self.execute_order(product_id, price)


