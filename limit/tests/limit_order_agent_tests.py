import unittest
from limit.limit_order_agent import LimitOrderAgent

class MockExecutionClient:
    def __init__(self):
        self.executed_orders = []

    def buy(self, product_id: str, amount: int):
        self.executed_orders.append((product_id, amount, 'buy'))

    def sell(self, product_id: str, amount: int):
        self.executed_orders.append((product_id, amount, 'sell'))

class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        """Set up for the test case."""
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_execution(self):
        """Test that a buy order is executed when the price drops below the limit."""
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.assertIn(('IBM', 1000, 'buy'), self.execution_client.executed_orders)
        self.assertEqual(len(self.agent.orders), 0)  # Order should be removed after execution

    def test_sell_order_execution(self):
        """Test that a sell order is executed when the price rises above the limit."""
        self.agent.add_order('sell', 'IBM', 500, 150)
        self.agent.on_price_tick('IBM', 151)
        self.assertIn(('IBM', 500, 'sell'), self.execution_client.executed_orders)
        self.assertEqual(len(self.agent.orders), 0)  # Order should be removed after execution

    def test_buy_order_not_executed(self):
        """Test that a buy order is not executed when the price does not reach the limit."""
        self.agent.add_order('buy', 'AAPL', 200, 120)
        self.agent.on_price_tick('AAPL', 121)
        self.assertNotIn(('AAPL', 200, 'buy'), self.execution_client.executed_orders)
        self.assertEqual(len(self.agent.orders), 1)  # Order should still be present

if __name__ == "__main__":
    unittest.main()
