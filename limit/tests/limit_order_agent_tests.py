import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def test_buy_order(self):

        exec_client = Mock()
        LOAgent = LimitOrderAgent(exec_client)

        # Buy order for IBM
        LOAgent.add_order(is_buy=True,product_id="IBM",
        amount=1000,price_limit=100)

        #Price is above the limit, order should not execute
        res=LOAgent.on_price_tick(product_id="IBM", price=110)
        self.assertFalse(res)

        #Price is below the limit, order should execute
        LOAgent.on_price_tick(product_id="IBM",price=80)
        self.assertTrue(res)
    

    def test_sell_order(self):
        exec_client = Mock()
        LOAgent = LimitOrderAgent(exec_client)

        # Add a sell order for NVIDIA
        LOAgent.add_order(is_buy=False,product_id="NVIDIA",
        amount=500,price_limit=150)

        #Price is below the limit,order should not execute
        res=LOAgent.on_price_tick(product_id="NVIDIA",price=120)
        self.assertFalse(res)

        #Price above the limit, order should execute
        LOAgent.on_price_tick(product_id="NVIDIA",price=151)
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
