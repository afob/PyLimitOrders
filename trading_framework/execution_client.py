from typing import Protocol



class ExecutionException(Exception):
    pass


class ExecutionClient(Protocol):

    def buy(self, product_id: str, amount: int):
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        print("Order: {} is bought for amount: {}".format(product_id, amount))
        ...

    def sell(self, product_id: str, amount: int):
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        print("Order: {} is sold for amount: {}".format(product_id, amount))
        ...
                
