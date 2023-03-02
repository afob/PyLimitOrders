from collections import defaultdict
from typing import Optional

from limit.config import PID_TO_WATCH, PRICE_LIMIT, AMOUNT_TO_BUY, TIMES_TO_EXECUTE
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.order_backlog = defaultdict(list)
        self.times_to_execute = TIMES_TO_EXECUTE

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        """Provides market data."""
        if product_id == PID_TO_WATCH and price <= PRICE_LIMIT and self.times_to_execute > 0:
            self.execution_client.buy(product_id, AMOUNT_TO_BUY)
            self.times_to_execute -= 1
        self.handle_order_backlog(product_id, price)

    def handle_order_backlog(self, product_id, price):
        if self.order_backlog:
            for product_id, orders_info in self.order_backlog.items():
                for order_info in orders_info:
                    self.execute_order(order_info['is_buy_order'], order_info['product_id'], order_info['amount'],
                                       order_info['limit'], price)

    def add_order(self, is_buy_order: bool, product_id: str, amount: int, limit: int = None):
        """Adds an order.
        The order type will be a market order (i.e., will execute immediately)
        if the limit argument is left unspecified.

        If a limit is specified, the order type will be a limit order
        (i.e., buy limit orders will only execute at the limit price or lower, and
        sell limit orders will only execute at the limit price or higher.)
        """

        # one limitation of the ExecutionClient is that it uses amounts that are integers...
        # wouldn't floats be a more logical choice, given that these are currency amounts?

        self.order_backlog[product_id].append({'is_buy_order': is_buy_order,
                                               'product_id': product_id,
                                               'amount': amount,
                                               'limit': limit})

    def execute_order(self, is_buy_order: bool, product_id: str, amount: int, limit: Optional[int] = None,
                      price: Optional[int] = None):
        if limit:
            self.execute_limit_order(amount, is_buy_order, product_id, limit, price)
        else:
            self.execute_market_order(amount, is_buy_order, product_id)

    def execute_market_order(self, amount, is_buy_order, product_id):
        if is_buy_order:
            self.execution_client.buy(product_id, amount)
        else:
            self.execution_client.sell(product_id, amount)

    def execute_limit_order(self, amount, is_buy_order, product_id, limit, price):
        if price:
            if is_buy_order and price <= limit:
                self.execution_client.buy(product_id, amount)
            elif not is_buy_order and price >= limit:
                self.execution_client.sell(product_id, amount)
        else:
            raise Exception("Limit order requested with no current price specified.")
