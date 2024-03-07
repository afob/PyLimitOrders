import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient, ExecutionException


class MockExecutionClient(ExecutionClient):
    """
    Mock implementation of ExecutionClient for testing purposes.
    """

    def __init__(self):
        self.executed_orders = []

    def buy(self, product_id: str, amount: int):
        self.executed_orders.append(('buy', product_id, amount))

    def sell(self, product_id: str, amount: int):
        self.executed_orders.append(('sell', product_id, amount))


class LimitOrderAgentTest(unittest.TestCase):

    def test_buy_order_triggered(self):
        """
        Test that a buy order is triggered when the price drops below $100 for IBM.
        """
        mock_execution_client = MockExecutionClient()
        agent = LimitOrderAgent(mock_execution_client)

        # Trigger a price drop below $100 for IBM
        agent.on_price_tick('IBM', 99.99)

        # Verify that a buy order is executed
        self.assertEqual(len(mock_execution_client.executed_orders), 1)
        self.assertEqual(mock_execution_client.executed_orders[0], ('buy', 'IBM', 1000))

    def test_add_and_execute_orders(self):
        """
        Test adding and executing buy/sell orders based on price ticks.
        """
        mock_execution_client = MockExecutionClient()
        agent = LimitOrderAgent(mock_execution_client)

        # Add buy and sell orders with different limits
        agent.add_order('buy', 'IBM', 1000, 98.0)  # Buy IBM when price <= $98
        agent.add_order('sell', 'IBM', 500, 105.0)  # Sell IBM when price >= $105

        # Trigger price ticks to execute orders
        agent.on_price_tick('IBM', 97.0)  # Price drops below $98, execute buy order
        agent.on_price_tick('IBM', 106.0)  # Price rises above $105, execute sell order

        # Verify executed orders
        self.assertEqual(len(mock_execution_client.executed_orders), 2)
        self.assertEqual(mock_execution_client.executed_orders[0], ('buy', 'IBM', 1000))
        self.assertEqual(mock_execution_client.executed_orders[1], ('sell', 'IBM', 500))

    def test_execution_failure_handling(self):
        """
        Test handling of execution failure when executing orders.
        """
        mock_execution_client = MockExecutionClient()
        agent = LimitOrderAgent(mock_execution_client)

        # Add a buy order
        agent.add_order('buy', 'IBM', 1000, 98.0)

        # Simulate execution failure
        # mock_execution_client.buy = lambda product_id, amount: raise ExecutionException("Execution failed")
        mock_execution_client.buy = lambda _, __: self._raise_execution_exception("Execution failed")

        # Trigger price tick to execute order
        agent.on_price_tick('IBM', 97.0)

        # Verify that the order remains in the queue
        self.assertEqual(len(agent.orders), 1)

    def test_edge_case_price_matching_limit(self):
        """
        Test scenario where price exactly matches the limit for an order.
        """
        mock_execution_client = MockExecutionClient()
        agent = LimitOrderAgent(mock_execution_client)

        # Add a buy order with a limit price
        agent.add_order('buy', 'IBM', 1000, 100.0)

        # Trigger price tick where the price exactly matches the limit
        agent.on_price_tick('IBM', 100.0)

        # Verify that the buy order is executed
        self.assertEqual(len(mock_execution_client.executed_orders), 1)
        self.assertEqual(mock_execution_client.executed_orders[0], ('buy', 'IBM', 1000))

    # Helper function to raise ExecutionException
    def _raise_execution_exception(message):
        raise ExecutionException(message)


if __name__ == '__main__':
    unittest.main()
