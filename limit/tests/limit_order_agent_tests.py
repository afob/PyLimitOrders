import unittest
from unittest.mock import MagicMock
import os
print("Current Working Directory:", os.getcwd()) 
import sys
print("sys.path::", sys.path)

# #from limit.limit_order_agent import LimitOrderAgent, LimitOrder, ExecutionException
# #from ..limit_order_agent import LimitOrderAgent, LimitOrder, ExecutionException
# from .limit_order_agent import LimitOrderAgent, LimitOrder, ExecutionException 




class LimitOrderAgentTest(
    unittest.TestCase):
    """
    Tests for the LimitOrderAgent class.
    """

    def setUp(self):
        """
        Creates a mock ExecutionClient and a LimitOrderAgent instance for testing.
        """
        self.mock_execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_add_order(self):
        """
        Tests that orders are correctly added to the agent's order book.
        """
        # Buy order
        self.agent.add_order(True, "IBM", 1000, 99.5)
        self.assertEqual(len(self.agent._orders), 1)
        buy_order = self.agent._orders[0]
        self.assertTrue(buy_order.buy_sell_flag)
        self.assertEqual(buy_order.product_id, "IBM")
        self.assertEqual(buy_order.amount, 1000)
        self.assertEqual(buy_order.limit_price, 99.5)

        # Sell order
        self.agent.add_order(False, "AAPL", 500, 150.0)
        self.assertEqual(len(self.agent._orders), 2)
        sell_order = self.agent._orders[1]
        self.assertFalse(sell_order.buy_sell_flag)
        self.assertEqual(sell_order.product_id, "AAPL")
        self.assertEqual(sell_order.amount, 500)
        self.assertEqual(sell_order.limit_price, 150.0)

    def test_on_price_tick_execution(self):
        """
        Tests order execution at or within limit prices.
        """
        # Buy order execution
        self.agent.add_order(True, "IBM", 1000, 100.0)
        self.agent.on_price_tick("IBM", 99.5)  # Triggers buy 
        self.mock_execution_client.buy.assert_called_once_with("IBM", 1000)

        # Sell order execution
        self.agent.add_order(False, "AAPL", 50, 145.0)
        self.agent.on_price_tick("AAPL", 150.0)  # Triggers sell
        self.mock_execution_client.sell.assert_called_once_with("AAPL", 50)

    def test_on_price_tick_no_execution(self):
        """
        Tests that orders are not executed if the price limit is not met.
        """
        self.agent.add_order(True, "IBM", 800, 90.0)
        self.agent.on_price_tick("IBM", 91.0)  # Above limit, no buy
        self.mock_execution_client.buy.assert_not_called()

        self.agent.add_order(False, "MSFT", 100, 180.0)
        self.agent.on_price_tick("MSFT", 175.0)  # Below limit, no sell
        self.mock_execution_client.sell.assert_not_called()

    def test_buy_execution_failure(self):
        """
        Tests handling ExecutionException during buy attempt.
        """
        self.agent.add_order(True, "IBM", 200, 100)
        self.mock_execution_client.buy.side_effect = ExecutionException("Simulated failure")
        self.agent.on_price_tick("IBM", 95)  
        self.assertFalse(self.agent._orders[0].filled)

    def test_filled_order_removal(self):
        """
        Tests that filled orders are removed from the order book.
        """
        self.agent.add_order(True, "MSFT", 50, 200)
        self.agent.on_price_tick("MSFT", 190)  # Executes the order
        self.assertEqual(len(self.agent._orders), 0)  

if __name__ == '__main__':
    unittest.main()
