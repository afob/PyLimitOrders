import unittest

from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionException


class MockExecutionClient:
    """Mock implementation of ExecutionClient for testing purposes."""

    def __init__(self):
        self.executed_orders = {"buy": [], "sell": []}

    def buy(self, product_id: str, amount: int) -> None:
        """Mock buy implementation."""
        if amount <= 0:
            raise ExecutionException("Amount to buy must be positive.")
        self.executed_orders["buy"].append((product_id, amount))

    def sell(self, product_id: str, amount: int) -> None:
        """Mock sell implementation."""
        if amount <= 0:
            raise ExecutionException("Amount to sell must be positive.")
        self.executed_orders["sell"].append((product_id, amount))

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.mock_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.mock_client)

    def test_buy_order_execution(self):
        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.on_price_tick(product_id="IBM", price=99)
        self.assertIn(("IBM", 1000), self.mock_client.executed_orders["buy"])
        self.assertEqual(len(self.agent.orders), 0)

    def test_sell_order_execution(self):
        self.agent.add_order(buy=False, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.on_price_tick(product_id="IBM", price=101)
        self.assertIn(("IBM", 1000), self.mock_client.executed_orders["sell"])
        self.assertEqual(len(self.agent.orders), 0)


# if __name__ == '__main__':
#     unittest.main()
