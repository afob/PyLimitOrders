import unittest
from unittest.mock import MagicMock
from trading_framework.execution_client import ExecutionClient
from  limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        # Create a mock ExecutionClient
        self.execution_client = MagicMock()
        # Instantiate LimitOrderAgent with the mock ExecutionClient
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_order(self):
        # Add a buy order
        self.agent.add_order("BUY", "IBM", 100.0, 90)
        # Add a sell order
        self.agent.add_order("SELL", "IBM2", 110.0, 120)
        
        # Assert that orders were added correctly
        self.assertEqual(len(self.agent.orders), 2)
        self.assertEqual(self.agent.orders[0]['Product_id'], "IBM")
        self.assertEqual(self.agent.orders[1]['flag'], "SELL")

    def test_execute_order_buy(self):
        # Add a buy order
        self.agent.add_order("BUY", "IBM", 100.0, 90)
        
        # Execute the buy order with a price lower than the limit
        self.agent.execute_order("IBM", 80.0)
        
        # Assert that the buy method of ExecutionClient was called with the correct arguments
        self.execution_client.buy.assert_called_once_with("IBM", 100.0)

    def test_execute_order_sell(self):
        # Add a sell order
        self.agent.add_order("SELL", "IBM2", 110.0, 120)
        
        # Execute the sell order with a price higher than or equal to the limit
        self.agent.execute_order("IBM2", 130.0)
        
        # Assert that the sell method of ExecutionClient was not called
        self.execution_client.sell.assert_not_called()

    def test_execute_order_no_matching_product_id(self):
        # Add a sell order
        self.agent.add_order("SELL", "IBM2", 110.0, 120)
        
        # Execute the order with a non-existing product ID
        self.agent.execute_order("non_existing_product_id", 130.0)
        
        # Assert that "Product Id does not exist" was printed
        self.assertTrue("Product Id does not exist" in self.agent.logs)

if __name__ == '__main__':
    unittest.main()
