from typing import Protocol


class ExecutionException(Exception):
    """Exception raised for errors in the execution of orders."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ExecutionClient(Protocol):

    def buy(self, product_id: str, amount: int):
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        try:
            print("Executing buy order for {0} shares of {1}".format(amount,product_id))
        except ExecutionException as e:
            print("An error occurred:", e)

    def sell(self, product_id: str, amount: int):
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        try:
            print("Executing sell order for {0} shares of {1}".format(amount,product_id))
        except ExecutionException as e:
            print("An error occurred:", e)
