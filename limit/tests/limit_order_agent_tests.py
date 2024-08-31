import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class MockExecutionClient(ExecutionClient):
    def __init__(self):
        self.executed_orders = []

    def execute_order(self, product_id: str, amount: int, order_type: str) -> None:
        self.executed_orders.append((product_id, amount, order_type))


class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_order(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]['product_id'], 'IBM')

    def test_execute_buy_order(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.assertEqual(len(self.execution_client.executed_orders), 1)
        self.assertEqual(self.execution_client.executed_orders[0], ('IBM', 1000, 'buy'))

    def test_execute_sell_order(self):
        self.agent.add_order(False, 'IBM', 500, 150)
        self.agent.on_price_tick('IBM', 151)
        self.assertEqual(len(self.execution_client.executed_orders), 1)
        self.assertEqual(self.execution_client.executed_orders[0], ('IBM', 500, 'sell'))

    def test_no_execution_if_price_not_met(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 101)
        self.assertEqual(len(self.execution_client.executed_orders), 0)


if __name__ == "__main__":
    unittest.main()
