import unittest
from trading_framework.execution_client import ExecutionClient
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def test_part1(self):
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        self.assertEqual(limit_order_client.on_price_tick("IBM",99.0), ["IBM"])
        self.assertEqual(limit_order_client.on_price_tick("IBM",100.0), [])

    def test_part2(self):
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        limit_order_client.add_order(True, "ABC", 200, 100)
        limit_order_client.add_order(False, "ABC", 200, 100)
        self.assertEqual(limit_order_client.on_price_tick("ABC",100.0), ["ABC", "ABC"])
        limit_order_client.add_order(True, "ABC", 200, 100)
        limit_order_client.add_order(False, "ABC", 200, 100)
        self.assertEqual(limit_order_client.on_price_tick("ABC",99.0), ["ABC"])


if __name__ == '__main__':
    unittest.main()

