import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent


class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.execution_client_mock = Mock()
        self.agent = LimitOrderAgent(self.execution_client_mock)

    def test_buy_order(self):
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick("IBM", 99)
        self.execution_client_mock.buy.assert_called_once_with("IBM", 1000)
        #self.execution_client_mock.buy.assert_any_call("IBM", 1000)

    def test_sell_order_execution(self):
        self.agent.add_order("sell", "google", 2000, 1000)
        self.agent.on_price_tick("google", 1051)
        self.execution_client_mock.sell.assert_called_once_with("google", 2000)


    def test_order_not_executed(self):
        self.agent.add_order("buy", "fb", 300, 800)
        self.agent.on_price_tick("fb", 850)
        self.execution_client_mock.buy.assert_not_called()



if __name__ == '__main__':
    unittest.main()





