import unittest
from limit.limit_order_agent import ExecutionClientSample , LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def test_price_tick(self):
        limobject = LimitOrderAgent(ExecutionClientSample())
        testValue = limobject.on_price_tick('prod_1', 90)
        message = "output value is not true."
        self.assertTrue( testValue, message)

    def test_add_order_buy(self):
        limobject = LimitOrderAgent(ExecutionClientSample())
        testValue_buy = limobject.add_order('B', 'prod_2', 50 , 10)
        message = "output value is not true."
        self.assertTrue( testValue_buy, message)


    def test_add_order_sell(self):
        limobject = LimitOrderAgent(ExecutionClientSample())
        testValue_sell = limobject.add_order('S', 'prod_2', 15 , 10)
        message = "output value is not true."
        self.assertTrue( testValue_sell, message)



