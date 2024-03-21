import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.execution_client = MagicMock()
        self.limit_order_agent = LimitOrderAgent(self.execution_client)

    def test_buy_ibm_below_100(self):
        self.execution_client.price_tick.return_value = 99.0
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.execution_client.buy.assert_called_once_with('IBM', 1000)

    def test_add_order(self):
        self.limit_order_agent.add_order(True, 'AAPL', 500, 150.0)
        self.limit_order_agent.add_order(False, 'GOOG', 200, 2500.0)
        self.assertEqual(len(self.limit_order_agent.held_orders), 2)
        self.assertEqual(self.limit_order_agent.held_orders[0], (True, 'AAPL', 500, 150.0))
        self.assertEqual(self.limit_order_agent.held_orders[1], (False, 'GOOG', 200, 2500.0))

    def test_execute_held_orders(self):
        self.execution_client.price_tick.side_effect = [149.0, 151.0, 2499.0, 2501.0]
        self.limit_order_agent.add_order(True, 'AAPL', 500, 150.0)
        self.limit_order_agent.add_order(False, 'GOOG', 200, 2500.0)
        self.limit_order_agent.on_price_tick('AAPL', 149.0)  # Market price reaches the buy limit for AAPL
        self.limit_order_agent.on_price_tick('GOOG', 2501.0)  # Market price reaches the sell limit for GOOG
        self.execution_client.buy.assert_called_once_with('AAPL', 500, 150.0)
        self.execution_client.sell.assert_called_once_with('GOOG', 200, 2500.0)

if __name__ == '__main__':
    unittest.main()


