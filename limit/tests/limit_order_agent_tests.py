import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ConcreteExecutionClient, ExecutionException

class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        # Creating a mock for ConcreteExecutionClient
        self.mock_client = Mock(spec=ConcreteExecutionClient)
        self.agent = LimitOrderAgent(self.mock_client)

    def test_add_order(self):
    
        self.agent.add_order('buy', 'IBM', 1000, 99.50)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0], ('buy', 'IBM', 1000, 99.50))

    def test_on_price_tick_buy_order(self):

        self.agent.add_order('buy', 'IBM', 1000, 99.50)
        self.agent.on_price_tick('IBM', 99.00)
        self.mock_client.buy.assert_called_once_with('IBM', 1000)
        self.assertEqual(len(self.agent.orders), 0)  # Order should be removed after execution

    def test_on_price_tick_sell_order(self):

        self.agent.add_order('sell', 'IBM', 1000, 100.50)
        self.agent.on_price_tick('IBM', 101.00)
        self.mock_client.sell.assert_called_once_with('IBM', 1000)
        self.assertEqual(len(self.agent.orders), 0)  # Order should be removed after execution

    def test_on_price_tick_no_action(self):
    
        self.agent.add_order('buy', 'IBM', 1000, 99.50)
        self.agent.on_price_tick('IBM', 100.00)
        self.mock_client.buy.assert_not_called()
        self.assertEqual(len(self.agent.orders), 1)  # Order should still be present

    def test_handle_execution_exception(self):

        self.mock_client.buy.side_effect = ExecutionException("Failed to execute buy order")
        self.agent.add_order('buy', 'IBM', 1000, 99.50)
        with self.assertRaises(ExecutionException):
            self.agent.on_price_tick('IBM', 99.00)

if __name__ == '__main__':
    unittest.main()

