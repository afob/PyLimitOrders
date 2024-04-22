import unittest
from unittest.mock import Mock
from trading_framework.execution_client import ExecutionClient
from  limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_mock = Mock(spec=ExecutionClient)
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order_buy(self):
        order_type = "BUY"
        product_id = "IBM"
        price = 50.0
        limit = 10
        self.limit_order_agent.add_order(order_type, product_id, price, limit)
        self.assertTrue(any(order['flag'] == 'BUY' for order in self.limit_order_agent.orders))

    def test_add_order_sell(self):
        order_type = "SELL"
        product_id = "IBM"
        price = 120.0
        limit = 5
        self.limit_order_agent.add_order(order_type, product_id, price, limit)
        self.assertTrue(any(order['flag'] == 'SELL' for order in self.limit_order_agent.orders))


    def test_execute_order(self):
        # Create a mock execution client
        execution_client = Mock(spec=ExecutionClient)

        # Create a LimitOrderAgent instance
        limit_order_agent = LimitOrderAgent(execution_client)

        # Add mock orders
        limit_order_agent.add_order("BUY", "IBM", 110, 120)
        limit_order_agent.add_order("SELL", "IBM2", 90, 80)

        # Set market price
        limit_order_agent.market_price = 100

        # Execute orders
        limit_order_agent.execute_order()
        
        execution_client.buy.assert_called_with("IBM", 110)
        execution_client.sell.assert_called_with("IBM2", 90)

if __name__ == '__main__':
    unittest.main()
