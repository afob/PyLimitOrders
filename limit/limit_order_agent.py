from trading_framework.execution_client import ExecutionClient, Protocol
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = list()

    def on_price_tick(self, product_id: str, price: float):
        """
        To place an order either buy or sell 
        :param product_id: the product to buy/sell
        :param price: price of the product
        :return: list of success products bought or sold
        """
        ### Part 1 Starts Here ###
        success = []
        if product_id == "IBM" and price < 100.0:
            self.execution_client.buy(self, product_id=product_id, amount=1000)
            success.append(product_id)
            return success
        ### Part 1 Ends Here ###

        ### Part 2 Starts Here ###
        temp_order = self.orders.copy()
        for order in temp_order:
            if order[1] == product_id and order[0] == True and order[3] <= price:
                self.execution_client.buy(self, product_id=order[1], amount=order[2])
                self.orders.remove(order)
                success.append(product_id)
            elif order[1] == product_id and order[0] == False and order[3] >= price:
                self.execution_client.sell(self, product_id=order[1], amount=order[2])
                self.orders.remove(order)
                success.append(product_id)
        return success


    def add_order(self, buy: bool, product_id: str, amount:int, limit:float):
        """
        To add an order in to order list
        :param buy: to indicate buy/sell the order. if it's true it's buy if it's false sell 
        :param product_id: the product to buy/sell
        :param amount: amount of the product
        :param limit: when needs to buy/sell
        :return: None
        """
        self.orders.append((buy, product_id, amount, limit))
    ### Part 2 Ends Here ###

        



            
