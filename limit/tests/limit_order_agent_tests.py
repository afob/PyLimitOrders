import unittest
from unittest.mock import MagicMock
import path
import sys
from flag import FLAG
 
# directory reach
directory = path.Path(__file__).abspath()
 
from .trading_framework.execution_client import ExecutionClient

sys.path.append(directory.parent.parent)
from limit.order import Order

## test for on_price_tick() function
class OrderTest(unittest.TestCase):
    def test_place_order_buy(self):
        thing = ExecutionClient()
        thing.buy = MagicMock(return_value=None)
        self.assertTrue(Order.place_order('IBM', 100.0, 1000, FLAG.BUY))

    def test_place_order_buy_1(self):
        thing = ExecutionClient()
        thing.buy = MagicMock(return_value=None)
        self.assertFalse(Order.place_order('IBM', 100.0, 0, FLAG.BUY))

    def test_place_order_sell(self):
        thing = ExecutionClient()
        thing.buy = MagicMock(return_value=None)
        self.assertTrue(Order.place_order('IBM', 150.0, 100, FLAG.SELL))

