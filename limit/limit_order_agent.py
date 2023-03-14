from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener

from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)


class OrderType(Enum):
    Buy = 'BUY'
    Sell = 'SELL'


class OrderStatus(Enum):
    Bought = 'BOUGHT'
    Sold = 'SOLD'


@dataclass
class Order:
    """
    Class :Order Entity
    :param order_type:  Buy| Sell
    :param product_id : product ID
    :param amount: amount of stock
    :param limit: limit on price to Buy or sell stock
    :param status: status of the order , initially None
    """
    order_type: str
    product_id: str
    amount: int
    limit: float
    status: str = None


class OrderExecutionClient(ExecutionClient):
    """
    Class: Implements ExecutionClient interface
    """
    def buy(self, product_id: str, amount: int):
        logging.info(f'BUY order Executed for: product: {product_id} amount: {amount}')

    def sell(self, product_id: str, amount: int):
        logging.info(f'SELL order Executed for: product:{product_id} amount: {amount}')


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param order : order entity
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.order = None
        self.execution_client = execution_client
        super().__init__()

    def on_price_tick(self, product_id: str, price: float):
        """
        Function: implements priceListener->on_price_tick, Decides
        :param product_id:
        :param price:
        :return: None
        """
        logging.info(f'Market Data : product:{product_id} change price: {price}')
        if (product_id == self.order.product_id) and (not self.order.status):
            if self.order.limit >= price and self.order.order_type == OrderType.Buy:
                self.execute_order(OrderType.Buy)
            elif self.order.limit <= price and self.order.order_type == OrderType.Sell:
                self.execute_order(OrderType.Sell)
        else:
            logging.info(f'product: {product_id} unavailable ')

    def add_order(self, order_type, product_id, amount, limit):
        """
        Function : Creates an order Entity
        :param order_type:
        :param product_id:
        :param amount:
        :param limit:
        :return: None
        """
        self.order = Order(order_type, product_id, amount, limit)

    def execute_order(self, order_type):
        """
        Function : Delegates OrderType to Execution Client-> buy|sell
        :param order_type:
        :return: None
        """
        if order_type == OrderType.Buy:
            try:
                self.execution_client.buy(self.order.product_id, self.order.amount)
                self.order.status = OrderStatus.Bought
            except ExecutionException as e:
                raise f'Failure in executing Buy for the Order'
        elif order_type == OrderType.Sell:
            try:
                self.execution_client.sell(self.order.product_id, self.order.amount)
                self.order.status = OrderStatus.Sold
            except ExecutionException as e:
                raise f'Failure in executing Sell for the Order'
        logging.info(f'Order Executed: {self.order}')

