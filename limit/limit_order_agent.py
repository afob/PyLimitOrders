from itertools import product

from limit.flag import Flag
from limit.orders import Order
from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
from collections import defaultdict
import logging

class InputValue(object):
        def _init(self, value):
            self.value = value

        def validate_string(self, exception, default=None):
            if self.value:
                self.value = str(self.value)
                self.value = self.value.strip()
            else:
                self.value = default.strip() if default is not None else ''
                raise exception

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        # TODO: Rebuild orders from a cache
        self.execution_client = execution_client
        self.order_queue = defaultdict(list)
        #self.orders = []
        #super().__init__()

        # Add buy order from README
        #self.add_order(Flag.BUY, 'IBM', 1000, 100.00)

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        pass
        # execute orders which match conditions in order they were created
        #pending = [Order(Flag.BUY, product_id='IBM', amount=1000, limit=100.00)]
        #pending = self.order_queue[product_id]

        #if len(pending) == 0:
        #return True

        for order in self.order_queue:
            print(self.order_queue)
            if order.Flag == Flag.BUY:
                # Submit buy orders if the newly ticked price is lower than the specified limit
                if order.limit >= price:
                    try:
                        self.execution_client.buy(order.product_id, order.amount)
                        #log the successfull execution of the trade
                        logging.info('Buy Order {} Filled! Product: {} Quantity: {}, Amount: {}'
                                     .format(order.id, product_id, order.amount, price))
                        self.remove_order(order.product_id, order.id)
                    except ExecutionException as e:
                        # log the exception caused
                        logging.warning("{} Buy order not executed due to exception! Order id: {} Product: {} "
                                        "Quantity: {}".format(e, order.id, order.product_id, order.amount))
                        return False

            elif order.flag == Flag.SELL:
                # Submit sell order if the newly ticked price is higher than the specified limit
                if order.limit <= price:
                    try:
                        self.execution_client.sell(order.product_id, order.amount)
                        # log the successfull execution of the trade
                        logging.info('Sell Order {} Filled! Product: {} Quantity: {}, Amount: {}'
                                     .format(order.id, product_id, order.amount, price))
                        self.remove_order(order.product_id, order.id)
                    except ExecutionException as e:
                        # log the exception caused
                        logging.warning("{} Sell order not executed due to exception! Order id: {} Product: Quantity: "
                                        "{}".format(e, order.id, order.product_id, order.amount))
                        return False

    def add_order(self, flag: Flag, product_id: str, amount: int, limit: float):
        """
        Adds order to open orders
        :param flag: order type (Buy or sell)
        :param product_id: ticker symbol
        :param amount: amount of shares to buy
        :param limit: price limit of order
        :return: None
        """
        product_id = product_id
        if amount<=0:
            raise ValueError ('Amount must be a positive number greater than zero.')
        if limit<=0:
            raise ValueError ('Amount must be a positive number greater than zero.')

        order = Order(flag, product_id, amount, limit)
        self.order_queue[product_id].append(order)

        #self.orders.append({"flag": BUY,"product_id": product_id,"amount": amount,"limit": limit,})

    def remove_order(self, product_id: str, id: str):
        """
        Remove order from queue
        :param product_id: ticker symbol
        :param id: uuid of order
        :return: None
        """
        self.order_queue[product_id] = [order for order in self.order_queue[product_id] if order.id == id]


