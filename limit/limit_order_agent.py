from limit.flag import Flag
from limit.order import Order
from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
from collections import defaultdict
import logging


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        # TODO: Rebuild orders from a cache
        self.execution_client = execution_client
        self.order_queue = defaultdict(list)

        # Add buy order from README
        self.add_order(Flag.BUY, 'IBM', 1000, 100.00)

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        # check order queue for pending orders

        pending = sorted(self.order_queue[product_id], key=lambda order: order.time_created)

        # execute orders which match conditions in order they were created

        if len(pending) == 0:
            return True

        for order in pending:
            if order.flag == Flag.BUY:
                # Submit buy orders if the newly ticked price is lower than the specified limit
                if order.limit >= price:
                    try:
                        self.execution_client.buy(order.product_id, order.amount)
                        logging.info('Buy Order {} Filled! Product: {} Quantity: {}, Amount: {}'
                                     .format(order.id, product_id, order.amount, price))
                        self.remove_order(order.product_id, order.id)
                    except ExecutionException as e:
                        logging.warning("{} Buy order not executed due to exception! Order id: {} Product: {} "
                                        "Quantity: {}".format(e, order.id, order.product_id, order.amount))
                        return False

            elif order.flag == Flag.SELL:
                # Submit sell order if the newly ticked price is higher than the specified limit
                if order.limit <= price:
                    try:
                        self.execution_client.sell(order.product_id, order.amount)
                        logging.info('Sell Order {} Filled! Product: {} Quantity: {}, Amount: {}'
                                     .format(order.id, product_id, order.amount, price))
                        self.remove_order(order.product_id, order.id)
                    except ExecutionException as e:
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
        order = Order(flag, product_id, amount, limit)
        self.order_queue[product_id].append(order)

    def remove_order(self, product_id: str, id: str):
        """
        Remove order from queue
        :param product_id: ticker symbol
        :param id: uuid of order
        :return: None
        """
        self.order_queue[product_id] = [order for order in self.order_queue[product_id] if order.id == id]
