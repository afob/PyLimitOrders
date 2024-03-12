import unittest
from limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient, ExecutionException
from unittest.mock import Mock


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_test = ExecutionClient
        self.limitagent = LimitOrderAgent(self.execution_client_test)

    #Validating number of orders added
    def test_add_order_method(self):
        #Testing number of orders added.
        self.limitagent.add_order(True, "IBM", 1000, 100.0)
        self.limitagent.add_order(True, "IBM", 1000, 100.0)
        self.assertEqual(len(self.limitagent.order_products), 2)
        self.assertEqual(self.limitagent.order_products[0], (True, "IBM", 1000, 100.0))

    #Validating buy scenario
    def test_execute_orders_buy(self):
        self.limitagent.add_order(True, "Accenture", 1000, 100.0)
        self.limitagent.on_price_tick("Accenture", 99.0)
        self.assertEqual(self.limitagent.status, "Brought")
        self.assertEqual(len(self.limitagent.order_products), 1)

    #Validating sell scenario
    def test_execute_orders_sell(self):
        self.limitagent.add_order(False, 'EY', 1000, 101.0)
        self.limitagent.on_price_tick('EY', 102.0)
        self.assertEqual(self.limitagent.status, "Sold")
        self.assertEqual(len(self.limitagent.order_products), 0)

    #Validating sell scenario at same limit, price
    def test_execute_orders_sell_same_limit(self):
        self.limitagent.add_order(False, 'IBM', 1000, 102.0)
        self.limitagent.on_price_tick('IBM', 102.0)
        self.assertEqual(self.limitagent.status, "Sold")
        self.assertEqual(len(self.limitagent.order_products), 0)


    #Validating buy scenario at same limit, price
    def test_execute_orders_buy_same_limit(self):
        self.limitagent.add_order(True, 'IBM', 1000, 101.0)
        self.limitagent.on_price_tick('IBM', 101.0)
        self.assertEqual(self.limitagent.status, "Hold")


    '''
    To run the below exceptions, uncomment `raise` line of code in limit_order_agent.py
    '''
    #validating buy exception
    def test_execute_orders_buy_exception(self):
        self.limitagent.add_order(True, "Accenture", 1000, 100.0)
        self.limitagent.on_price_tick("Accenture", 99.0)
        self.assertEqual(self.limitagent.status, 'Failed to buy')
        self.assertEqual(len(self.limitagent.order_products), 1)

    #validating sell exception
    def test_execute_orders_sell_exception(self):
        self.limitagent.add_order(False, 'EY', 1000, 101.0)
        self.limitagent.on_price_tick('EY', 102.0)
        self.assertEqual(self.limitagent.status, 'Failed to sell')
        self.assertEqual(len(self.limitagent.order_products), 0)


if __name__ == '__main__':
    unittest.main()



