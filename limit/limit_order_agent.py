from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
import random


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
        return price
        # return self.execute_order(product_id, price)

    def add_order(self, flag: str, product_id: str, amount: int, limit: int):
        """
        method to accept order
        :param flag: indicates whether to buy or sell
        :param product_id: the product to buy
        :param amount: the amount to buy
        :param limit: the limit at which to buy or sell
        Author: Priyanka Nesargi
        """
        try:
            if flag in ['buy', 'sell']:
                self.orders.append({'flag': flag, 'product_id': product_id, 'amount': amount, 'limit': limit, 'is_executed':False})
                print(self.orders, "order added successfully")
                return True
            else:
                print({'flag': flag, 'product_id': product_id, 'amount': amount, 'limit': limit}, "Order not added because of Invalid Flag")
                return True
        except Exception as e:
            print(str(e))
            raise ExecutionException

    def execute_order(self, product_id: str, price: float):
        """
        method to buy or sell order
        :param product_id: the product to buy
        :param price: the current market price of the product
        Author: Priyanka Nesargi
        """
        try:
            # Implement LimitOrderAgent such that it buys 1000 shares of IBM when the price drops below $100
            # if product_id == 'IBM' and float(price) < float(100):
            #     self.execution_client.buy(product_id, 1000)
            price = self.on_price_tick(product_id, price)
            # orders consists only orders which are of requested product id reducing looping and checking if the proudct id matches with requested product id so to reduce loop i have used filter 
            # orders = list(filter(lambda x: x.get('product_id', '')==product_id, self.orders))
            orders = list(filter((lambda x:x.get('product_id', '')==product_id and x.get('is_executed')==False), self.orders))
            print(orders)
            for order in orders:
                if order['flag'] == 'buy' and float(price) <= float(order['limit']):
                    self.execution_client.buy(self,order['product_id'], order['amount'])
                    order['is_executed'] = True
                    print(order)
                    print("{0} amount of {1} bought successfully at {2} price".format(order['amount'], order['product_id'], price))   
                elif order['flag'] == 'sell' and float(price) >= float(order['limit']):
                    self.execution_client.sell(self,order['product_id'], order['amount'])
                    order['is_executed'] = True
                    print(order)
                    print("{0} amount of {1} sold successfully at {2} price".format(order['amount'], order['product_id'], price))
                else:
                    print("{0} amount of {1} does not satisfy {2} price which was placed at limit {3}".format(order['amount'], order['product_id'], price, order['limit']))
            # if required to remove from list then we can remove orders which ever is_executed status is True
            # here i am filtering the orders list and storing only orders which have is_executed status False
            # self.orders = list(filter(lambda x: x.get('is_executed', '')==False, self.orders))
            return True
        
        except Exception as e:
            print(str(e))
            raise ExecutionException




        
        
