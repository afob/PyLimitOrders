import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.mock_execution_client = Mock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_below_threshold(self):
        self.agent.on_price_tick("IBM", 99)
        self.mock_execution_client.buy.assert_called_once_with("IBM", 1000)

    def test_do_not_buy_above_threshold(self):
        self.agent.on_price_tick("IBM", 101)
        self.mock_execution_client.buy.assert_not_called()

    def test_add_and_process_order(self):
        # Add a limit buy order
        self.agent.add_order(buy=True, product_id="AAPL", amount=500, limit_price=150)
        self.agent.current_price = 140  # Simulate price update
        self.agent.process_orders()
        self.mock_execution_client.buy.assert_called_once_with("AAPL", 500)

    def test_add_and_process_sell_order(self):
        # Add a limit sell order
        self.agent.add_order(buy=False, product_id="AAPL", amount=500, limit_price=150)
        self.agent.current_price = 160  # Simulate price update
        self.agent.process_orders()
        self.mock_execution_client.sell.assert_called_once_with("AAPL", 500)

if __name__ == "__main__":
    unittest.main()
