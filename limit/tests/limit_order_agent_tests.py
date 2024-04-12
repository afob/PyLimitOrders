import unittest
from trading_framework.execution_client import ExecutionClient
from limit.limit_order_agent import LimitOrderAgent


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_mock = ExecutionClient
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order Passed Successfully")

    def test_execute_buy_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        res = self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.assertTrue(res)
        print("test_execute_buy_order Passed Successfully")

    def test_execute_sell_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 125.0)
        res = self.limit_order_agent.on_price_tick('IBM', 130.0)
        self.assertTrue(res)
        print("test_execute_sell_order Passed Successfully")

    def test_execute_bought_order(self):
        res = self.limit_order_agent.add_order('bought', 'IBM', 1000, 1001.0)
        self.assertTrue(res)
        print("test_execute_bought_order Passed Successfully")


