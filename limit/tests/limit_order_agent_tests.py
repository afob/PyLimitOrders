import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        self.execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_order(self):
        self.assertEqual(len(self.agent.held_orders), 0)
        self.agent.add_order('IBM', 1000, 99, 'BUY')
        self.assertEqual(len(self.agent.held_orders), 1)
    def test_execute_held_orders_buy(self):
        self.agent.add_order('IBM', 1000, 99, 'BUY')
        self.agent.on_price_tick = MagicMock(return_value=('IBM', 99))
        self.agent.execute_held_orders()
        self.execution_client.buy.assert_called_once_with('IBM', 1000)

    def test_execute_held_orders_sell(self):
        self.agent.add_order('IBM', 1000, 101, 'SELL')
        self.agent.on_price_tick = MagicMock(return_value=('IBM', 101))
        self.agent.execute_held_orders()
        self.execution_client.sell.assert_called_once_with('IBM', 1000)


if __name__ == '__main__':
    unittest.main()

