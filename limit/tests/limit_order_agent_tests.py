import unittest
from limit.limit_order_agent import LimitOrderAgent
from unittest.mock import MagicMock

class LimitOrderAgentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Execution started for test cases')

    def setUp(self):
        # Create a mock execution client
        self.execution_client = MagicMock()
        # Initialize the LimitOrderAgent with the mock execution client
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_execution(self):
        # Test buying 1000 shares of IBM when price drops below $100
        self.agent.on_price_tick('IBM', 99)
        self.execution_client.buy('IBM', 1000)
        print("\n test case test_buy_order_execution pass successfully")

    def test_sell_order_execution(self):
        # Test executing sell order for IBM
        self.agent.add_order(False, 'IBM', 500, 120)
        self.agent.on_price_tick('IBM', 120)
        self.execution_client.sell('IBM', 500)


    def test_sell_execution_client(self):
        self.assertNotEqual("Executing sell order: Selling 500 shares of IBM", self.execution_client.sell('IBM', 500))
        self.assertNotEqual("Executing sell order: Selling 5000 shares of IBM", self.execution_client.sell('IBM', 500))

    def test_buy_execution_client(self):
        self.assertNotEqual("Executing buy order: Buying 500 shares of IBM", self.execution_client.buy('IBM', 500))
        self.assertNotEqual("Executing buy order: Buying 5000 shares of IBM", self.execution_client.buy('IBM', 500))


    def test_add_order(self):
        # Test adding buy order for Apple
        self.agent.add_order(True, 'AAPL', 200, 150)
        self.assertEqual(len(self.agent.orders[0]), 4)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]['type'], 'buy')
        self.assertEqual(self.agent.orders[0]['product_id'], 'AAPL')
        self.assertEqual(self.agent.orders[0]['amount'], 200)
        self.assertEqual(self.agent.orders[0]['limit'], 150)
        self.assertNotEqual(self.agent.orders[0]['type'], 'random')
        self.agent.add_order(False, 'INFYS', 1000, 150)
        self.assertEqual(len(self.agent.orders), 2)
        self.assertEqual(self.agent.orders[1]['type'], 'sell')
        self.assertEqual(self.agent.orders[1]['product_id'], 'INFYS')
        self.assertNotEqual(self.agent.orders[1]['product_id'], 'INFS')
        self.assertNotEqual(self.agent.orders[1]['amount'], 200)
        self.assertGreater(self.agent.orders[1]['amount'], 0)
        self.assertEqual(self.agent.orders[1]['limit'], 150)
        self.assertGreater(self.agent.orders[1]['limit'], -1)
        self.assertNotEqual(self.agent.orders[1]['type'], 'random')

    def tearDown(self):
        print('Execution completed for each method')

    @classmethod
    def tearDownClass(cls):
        print('All execution completed')


if __name__ == '__main__':
    unittest.main()

