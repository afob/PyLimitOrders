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
        self.assertTrue(Order.place_order([{product_id: 'IBM', price_limit: 100.0, units: 1000, flag :True},{product_id: 'TATA', price_limit: 50.0, units: 500, flag :True}]))
        

    def test_place_order_buy_1(self):
        thing = ExecutionClient()
        thing.buy = MagicMock(return_value=None)
        self.assertFalse(Order.place_order([{product_id: 'IBM', price_limit: 100.0, units: 1000, flag :False},{product_id: 'TATA', price_limit: 50.0, units: 500, flag :False}]))

    def test_place_order_sell(self):
        thing = ExecutionClient()
        thing.buy = MagicMock(return_value=None)
        self.assertTrue(Order.place_order([{product_id: 'Honda', price_limit: 1400.0, units: 2500, flag :True},{product_id: 'NIFTY', price_limit: 500.0, units: 2500, flag :True}]))

