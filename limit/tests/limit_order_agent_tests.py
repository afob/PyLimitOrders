# Tests
import sys
import unittest
sys.path.append("C:/Users/HP/Desktop/Project/PyLimitOrders/trading_framework")
sys.path.append("C:/Users/HP/Desktop/Project/PyLimitOrders/limit")

from execution_client import ExecutionClient
from limit_order_agent import LimitOrderAgent

class Mockclient(ExecutionClient):

    def buy(self, product_id, amount):
        print(f"Bought total shares- {amount} of {product_id} company")

    def sell(self, product_id, amount):
        print(f"Sold total shares- {amount} of {product_id} company")

class LimitOrderAgentTest(unittest.TestCase):
    def test_limit_order_agent(self):
        mock_client = Mockclient()
        cust = LimitOrderAgent(mock_client)

        cust.add_order(True,'IBM', 1000, 99) #we want to uy at 99
        cust.on_price_tick('IBM', 100)  #and market is also set to 100, so this will not execute .
        print()
        cust.add_order(True,'IBM', 1000, 99)
        cust.on_price_tick('IBM', 99) #This will execute as market price is now set to 99 and limit is also 99

test=LimitOrderAgentTest()
test.test_limit_order_agent()







