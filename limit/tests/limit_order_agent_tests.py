import unittest
from limit_order_agent import LimitOrderAgent
from trading_framework import MockExecutionClient

class TestLimitOrderAgent(unittest.TestCase):
    
    def setUp(self):
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)
    
    def test_add_order(self):
        self.agent.add_order(True, "IBM", 1000, 100.0)
        self.assertEqual(len(self.agent.orders), 1)
    
    def test_price_tick_executes_buy_order(self):
        self.agent.add_order(True, "IBM", 1000, 100.0)
        self.agent.price_tick("IBM", 99.0)
        self.assertEqual(self.execution_client.executed_orders, [("IBM", 1000, "buy")])
        self.assertEqual(len(self.agent.orders), 0)
    
    def test_price_tick_executes_sell_order(self):
        self.agent.add_order(False, "IBM", 500, 150.0)
        self.agent.price_tick("IBM", 151.0)
        self.assertEqual(self.execution_client.executed_orders, [("IBM", 500, "sell")])
        self.assertEqual(len(self.agent.orders), 0)

if __name__ == "__main__":
    unittest.main()
