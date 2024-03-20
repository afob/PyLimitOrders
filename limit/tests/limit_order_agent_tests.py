from unittest import TestCase
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(TestCase):

    def test_something(self):
        self.execution_client=Mock()
        self.tester=LimitOrderAgent(self.execution_client)

    def test_add_orders(self):
        #ord_typ: str, ord_price: float, p_id: str,amount: float
        self.tester.orders('buy',100,'IBM',1000)
        self.assertEqual(len(self.tester.orders),1)

    def test_price_tik(self):
        self.tester.orders('buy',100,'IBM',1000)
        self.tester.on_price_tick('IBM',99)
        self.execution_client.buy.assert_called_once_with('IBM',1000)




