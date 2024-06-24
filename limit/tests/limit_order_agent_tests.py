import unittest

class LimitOrderAgentTest(unittest.TestCase):

    def test_add_order(self):
        # Initial length of orders list
        initial_length = len(self.agent.orders)

                self.agent.add_order(True, 'IBM', 1000, 100)

        # Verify that the order was added successfully
        self.assertEqual(len(self.agent.orders), initial_length + 1)
        new_order = self.agent.orders[-1]
        self.assertEqual(new_order['buy_flag'], True)
        self.assertEqual(new_order['product_id'], 'IBM')
        self.assertEqual(new_order['amount'], 1000)
        self.assertEqual(new_order['limit'], 100)

    def test_on_price_tick(self):
        # Add a buy order for IBM at $100
        self.agent.add_order(True, 'IBM', 1000, 100)

        self.agent.on_price_tick('IBM', 99)
        self.execution_client.buy.assert_called_once_with('IBM', 1000)

        self.agent.add_order(False, 'IBM', 1000, 130)
        self.agent.on_price_tick('IBM', 150)
        self.execution_client.sell.assert_called_once_with('IBM', 1000)
