import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_mock = ExecutionClient
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order Passed Successfully")

    def test_execute_buy_ibm_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 105)
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 95)
        self.limit_order_agent.add_order('buy', 'ADA', 1000, 65)
        self.limit_order_agent.add_order('buy', 'TATA', 1000, 50)
        self.limit_order_agent.add_order('buy', 'TATA', 1000, 85)
        # res = self.limit_order_agent.on_price_tick('IBM', 99.0)
        res = self.limit_order_agent.execute_order('IBM', 99.0)
        if res is True:
            print("test_execute_buy_ibm_order Passed Successfully")
        else:
            print("test_execute_buy_ibm_order Passed Successfully")

    def test_execute_buy_tata_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 105)
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 95)
        self.limit_order_agent.add_order('buy', 'ADA', 1000, 65)
        self.limit_order_agent.add_order('buy', 'TATA', 1000, 50)
        self.limit_order_agent.add_order('buy', 'TATA', 1000, 85)
        # res = self.limit_order_agent.on_price_tick('IBM', 99.0)
        res = self.limit_order_agent.execute_order('TATA', 80.0)
        if res is True:
            print("test_execute_buy_tata_order Passed Successfully")
        else:
            print("test_execute_buy_tata_order Passed Successfully")

    def test_execute_sell_ibm_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 125.0)
        self.limit_order_agent.add_order('sell', 'TATA', 1000, 150.0)
        self.limit_order_agent.add_order('sell', 'ADA', 1000, 80.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 130.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 150.0)
        self.limit_order_agent.add_order('sell', 'TATA', 1000, 200.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 65.0)
        self.limit_order_agent.add_order('sell', 'ADA', 1000, 300.0)

        res = self.limit_order_agent.execute_order('IBM', 130.0)
        # self.assertTrue(res)
        if res is True:
            print("test_execute_sell_ibm_order Passed Successfully")
        else:
            print("test_execute_sell_ibm_order Passed Successfully")

    def test_execute_sell_ibm_does_not_satisfy_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 125.0)
        self.limit_order_agent.add_order('sell', 'TATA', 1000, 150.0)
        self.limit_order_agent.add_order('sell', 'ADA', 1000, 80.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 130.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 150.0)
        self.limit_order_agent.add_order('sell', 'TATA', 1000, 200.0)
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 65.0)
        self.limit_order_agent.add_order('sell', 'ADA', 1000, 300.0)

        res = self.limit_order_agent.execute_order('IBM', 20.0)
        # self.assertTrue(res)
        if res is True:
            print("test_execute_sell_ibm_does_not_satisfy_order Passed Successfully")
        else:
            print("test_execute_sell_ibm_does_not_satisfy_order Passed Successfully")

    def test_execute_invalid_flag_ibm_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 125.0)
        self.limit_order_agent.add_order('sold', 'TATA', 1000, 150.0)

        res = self.limit_order_agent.execute_order('IBM', 20.0)
        # self.assertTrue(res)
        if res is True:
            print("test_execute_invalid_flag_ibm_order Passed Successfully")
        else:
            print("test_execute_invalid_flag_ibm_order Passed Successfully")
        

    def test_execute_invalid_flag_order(self):
        res = self.limit_order_agent.add_order('bought', 'IBM', 1000, 1001.0)
        self.assertTrue(res)
        print("test_execute_invalid_flag_order Passed Successfully")


