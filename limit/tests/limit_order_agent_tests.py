import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

class LimitOrderAgentTest(unittest.TestCase):

    def test_something(self):
        self.fail("not implemented error")

    def setUp(self):
        self.execution_client_mock = ExecutionClient
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 99.5)
        self.assertEqual(len(self.limit_order_agent.orders), 1)

    def test_execute_buy_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.7)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.assertTrue(self.limit_order_agent.orders)

    def test_execute_sell_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 101.0)
        self.limit_order_agent.on_price_tick('IBM', 102.0)
        self.assertFalse(self.limit_order_agent.orders)

    def test_execute_wrong_order(self):
        self.limit_order_agent.add_order('wrong', 'IBM', 1000, 101.0)
        self.limit_order_agent.on_price_tick('IBM', 103.0)
        self.assertTrue(self.limit_order_agent.orders)
