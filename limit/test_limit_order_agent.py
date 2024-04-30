import unittest
from unittest.mock import MagicMock

from limit.limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        self.execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_order(self):
        self.agent.add_order(True, 'BTC-USD', 10, 50000)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]['buy'], True)
        self.assertEqual(self.agent.orders[0]['product_id'], 'BTC-USD')
        self.assertEqual(self.agent.orders[0]['amount'], 10)
        self.assertEqual(self.agent.orders[0]['limit'], 50000)

    def test_price_tick_execute_buy(self):
        self.agent.add_order(True, 'BTC-USD', 10, 50000)
        self.agent.price_tick('BTC-USD', 49000)
        self.execution_client.execute_buy.assert_called_once_with('BTC-USD', 10)
        self.assertEqual(len(self.agent.orders), 0)

    def test_price_tick_execute_sell(self):
        self.agent.add_order(False, 'BTC-USD', 10, 50000)
        self.agent.price_tick('BTC-USD', 51000)
        self.execution_client.execute_sell.assert_called_once_with('BTC-USD', 10)
        self.assertEqual(len(self.agent.orders), 0)

    def test_price_tick_no_execution(self):
        self.agent.add_order(True, 'BTC-USD', 10, 50000)
        self.agent.price_tick('BTC-USD', 51000)
        self.execution_client.execute_buy.assert_not_called()
        self.assertEqual(len(self.agent.orders), 1)

if __name__ == '__main__':
    unittest.main()
