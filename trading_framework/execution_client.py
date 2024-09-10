from abc import abstractmethod
from typing import Protocol


class ExecutionException(Exception):
    pass


class ExecutionClient(Protocol):

    @abstractmethod
    def buy(self, product_id: str, amount: int):
        print('buy exeuted')
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def sell(self, product_id: str, amount: int):
        print('sell exeuted')
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        raise NotImplementedError