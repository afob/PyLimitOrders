import unittest
from unittest.mock import MagicMock
import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
from .trading_framework.execution_client import ExecutionClient

sys.path.append(directory.parent.parent)
from limit.order import Order

## test for on_price_tick() function
class OrderTest(unittest.TestCase):

    class LimitOrderAgentTest(unittest.TestCase):
        def test_place_order(self):
            thing = ExecutionClient()
            thing.buy = MagicMock(return_value=None)
            self.assertTrue(Order.place_order('IBM', 100.0, 1000, 'buy'))


