import unittest
from limit.limit_order_agent import LimitOrderAgent

class MockExecutionClient:
    def __init__(self):
        self.orders_executed = []

    def buy(self, product_id, amount):
        self.orders_executed.append(('buy', product_id, amount))

    def sell(self, product_id, amount):
        self.orders_executed.append(('sell', product_id, amount))

class LimitOrderAgentTest(unittest.TestCase):

    def test_buy_order_execution(self):
        client = MockExecutionClient()
        agent = LimitOrderAgent(client)
        agent.add_order(is_buy=True, product_id="IBM", amount=1000, limit=100)

        # Simulate a price tick
        agent.price_tick("IBM", 99)

        # Check that the buy order was executed
        self.assertEqual(len(client.orders_executed), 1)
        self.assertEqual(client.orders_executed[0], ('buy', "IBM", 1000))

    def test_sell_order_execution(self):
        client = MockExecutionClient()
        agent = LimitOrderAgent(client)
        agent.add_order(is_buy=False, product_id="AAPL", amount=500, limit=150)

        # Simulate a price tick
        agent.price_tick("AAPL", 151)

        # Check that the sell order was executed
        self.assertEqual(len(client.orders_executed), 1)
        self.assertEqual(client.orders_executed[0], ('sell', "AAPL", 500))

    def test_no_execution_when_price_does_not_meet_limit(self):
        client = MockExecutionClient()
        agent = LimitOrderAgent(client)
        agent.add_order(is_buy=True, product_id="GOOG", amount=200, limit=2500)

        # Simulate a price tick
        agent.price_tick("GOOG", 2501)

        # Check that no order was executed
        self.assertEqual(len(client.orders_executed), 0)

if __name__ == '__main__':
    unittest.main()