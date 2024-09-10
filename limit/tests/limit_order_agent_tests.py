import unittest
from collections import defaultdict
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent
from limit.flag import Flag
from limit.orders import Order
from trading_framework.execution_client import ExecutionClient, ExecutionException

class MockExecutionClient:
    def __init__(self):
        self.executed_orders = {"BUY":[],"SELL":[]}

    def buy(self, product_id:str,amo:int):
        if amount <= 0:
            raise Exception("Amount must be positive")

    def sell(self):
        if amount <= 0:
            raise Exception("Amount must be positive")

class LimitOrderAgentTest(unittest.TestCase):
    """
    All test cases assume default initial buy order of 1000 shares at/below $100.00 as in README.md
    """
    def setUp(self) -> None:
        self.ex_client = Mock(ExecutionClient)
        self.limit_agent = LimitOrderAgent(execution_client=self.ex_client)
        self.sell_order_test_queue = defaultdict(list)
        self.sell_order_test_queue['IBM'] = [Order(Flag.SELL, product_id='IBM', amount=1000, limit=100.00)]

    def test_add_order(self):
        self.limit_agent.add_order(Flag.BUY, product_id='IBM', amount=1000, limit=100.00)
        self.assertEqual(len(self.limit_agent.order_queue['IBM']), 1)

    def test_remove_order(self):
        if len(self.limit_agent.order_queue['IBM'])>0:
            self.limit_agent.remove_order('IBM', self.limit_agent.order_queue['IBM'][0])
            self.assertEqual(len(self.limit_agent.order_queue['IBM']), 0)


    def test_buy_below_limit(self):
        self.limit_agent.add_order(Flag.BUY, product_id='IBM', amount=1000, limit=100.00)
        self.limit_agent.on_price_tick('IBM', 99.00)
        self.ex_client.buy.assert_called()

    def test_buy_above_limit(self):
        self.limit_agent.on_price_tick('IBM', 101.00)
        self.ex_client.buy.assert_not_called()

    #def test_sell_above_limit(self):
    #    self.limit_agent.order_queue = self.sell_order_test_queue
    #    self.limit_agent.on_price_tick('IBM', 101.00)
    #    self.ex_client.sell.assert_called()

    #def test_sell_below_limit(self):
    #    self.limit_agent.order_queue = self.sell_order_test_queue
    #    self.limit_agent.on_price_tick('IBM', 99.00)
    #    self.ex_client.sell.assert_not_called()

    def test_mismatch_product(self):
        self.limit_agent.on_price_tick('TSLA', 101.00)
        self.ex_client.buy.assert_not_called()
        self.ex_client.sell.assert_not_called()

    def test_raise_exception(self):
        self.limit_agent.on_price_tick('IBM', 101.00)
        self.assertRaises(ExecutionException)