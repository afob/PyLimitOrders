import unittest

from limit.limit_order_agent import LimitOrderAgent, InputValue
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

    def test_invalid_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.agent.add_order(buy=True, product_id="IBM",
                                 amount=-1000, limit_price=100)

        with self.assertRaises(ValueError):
            self.agent.add_order(buy=False, product_id="IBM",
                                 amount=0, limit_price=100)

    def test_invalid_price_raises_exception(self):
        with self.assertRaises(ValueError):
            self.agent.add_order(buy=True, product_id="IBM",
                                 amount=1000, limit_price=-10)

        with self.assertRaises(ValueError):
            self.agent.add_order(buy=False, product_id="IBM",
                                 amount=1000, limit_price=0)

    def test_multiple_orders(self):
        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.add_order(buy=False, product_id="AAPL",
                             amount=500, limit_price=150)

        self.agent.on_price_tick(product_id="IBM", price=99)
        self.agent.on_price_tick(product_id="AAPL", price=151)

        self.assertIn(("IBM", 1000), self.mock_client.executed_orders["buy"])
        self.assertIn(("AAPL", 500), self.mock_client.executed_orders["sell"])
        self.assertEqual(len(self.agent.orders), 0)

    def test_no_execution_when_conditions_not_met(self):
        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.on_price_tick(product_id="IBM", price=101)
        self.assertNotIn(
            ("IBM", 1000), self.mock_client.executed_orders["buy"])
        self.assertEqual(len(self.agent.orders), 1)

    def test_order_removal_after_execution(self):
        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.on_price_tick(product_id="IBM", price=99)
        self.assertEqual(len(self.agent.orders), 0)


    def test_execution_exception_handling(self):
        with self.assertRaises(ValueError) as context:
            self.agent.add_order(buy=True, product_id="IBM",
                                amount=1000, limit_price=-100)

        self.assertEqual(str(context.exception),
                        'limit_price must be a positive number greater than zero.')


    def test_orders_for_different_products(self):
        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.add_order(buy=False, product_id="AAPL",
                             amount=500, limit_price=150)

        self.agent.on_price_tick(product_id="IBM", price=99)
        self.assertIn(("IBM", 1000), self.mock_client.executed_orders["buy"])
        self.assertNotIn(
            ("AAPL", 500), self.mock_client.executed_orders["sell"])
        self.assertEqual(len(self.agent.orders), 1)

    def test_execution_exception_does_not_remove_order(self):
        def mock_buy(product_id, amount):
            raise ExecutionException("Execution failed")

        self.mock_client.buy = mock_buy

        self.agent.add_order(buy=True, product_id="IBM",
                             amount=1000, limit_price=100)
        self.agent.on_price_tick(product_id="IBM", price=99)

        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]["product_id"], "IBM")
        self.assertEqual(self.agent.orders[0]["amount"], 1000)
        self.assertEqual(self.agent.orders[0]["limit_price"], 100)
        self.assertTrue(self.agent.orders[0]["buy"])


if __name__ == '__main__':
    unittest.main()
