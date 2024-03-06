import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

class MockExecutionClient(ExecutionClient):
    def buy(self, product_id: str, amount: int):
        pass
    def sell(self, product_id: str, amount: int):
        pass
        
class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        # self.mock_execution_client = MockExecutionClient()
        self.mock_execution_client = Mock(spec=ExecutionClient)
        self.limit_order_agent = LimitOrderAgent(self.mock_execution_client)
        
    def test_add_buy_order(self):
        self.limit_order_agent.add_order(is_buy=True, product_id="AAPL", amount=100, limit_price=150)
        self.mock_execution_client.buy.assert_called_with("AAPL", 100)

    def test_add_sell_order(self):
        self.limit_order_agent.add_order(is_buy=False, product_id="AAPL", amount=50, limit_price=200)
        self.mock_execution_client.sell.assert_called_with("AAPL", 50)

if __name__ == "__main__":
    unittest.main()

