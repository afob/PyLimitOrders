import unittest
from unittest.mock import Mock, patch

from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client = Mock(ExecutionClient)
        self.limit_order_agent = LimitOrderAgent(self.execution_client)

    @patch('limit.limit_order_agent.LimitOrderAgent')
    def test_add_order(self, mock):
        mock.add_order(is_buy_order=True, product_id="test", amount=42, limit=24)
        mock.add_order.assert_called_with(is_buy_order=True, product_id="test", amount=42, limit=24)

    def test_execute_buy_market_order(self):
        self.limit_order_agent.execute_order(is_buy_order=True, product_id="test", amount=42, limit=None)
        self.execution_client.buy.assert_called_with("test", 42)

    def test_execute_sell_market_order(self):
        self.limit_order_agent.execute_order(is_buy_order=False, product_id="test", amount=42, limit=None)
        self.execution_client.sell.assert_called_with("test", 42)

    def test_execute_buy_limit_order(self):
        self.limit_order_agent.execute_order(is_buy_order=True, product_id="test", amount=42, limit=100, price=99)
        self.execution_client.buy.assert_called_with("test", 42)

    def test_execute_sell_limit_order(self):
        self.limit_order_agent.execute_order(is_buy_order=False, product_id="test", amount=42, limit=100, price=101)
        self.execution_client.sell.assert_called_with("test", 42)

    def test_IBM_add_buy_order(self):
        self.limit_order_agent.add_order(is_buy_order=True, product_id="IBM", amount=1000, limit=100)
        self.assertEqual({'IBM': [{'is_buy_order': True, 'product_id': 'IBM', 'amount': 1000, 'limit': 100}]},
                         self.limit_order_agent.order_backlog)

    def test_IBM_add_sell_order(self):
        self.limit_order_agent.add_order(is_buy_order=False, product_id="IBM", amount=1000, limit=100)
        self.assertEqual({'IBM': [{'is_buy_order': False, 'product_id': 'IBM', 'amount': 1000, 'limit': 100}]},
                         self.limit_order_agent.order_backlog)

    def test_check_existing_backlog_with_limit_order_with_no_price(self):
        self.limit_order_agent.order_backlog = {
            'IBM': [{'is_buy_order': True, 'product_id': 'IBM', 'amount': 1000, 'limit': 100}]}

        with self.assertRaises(Exception):
            self.limit_order_agent.handle_order_backlog('IBM', None)

    def test_check_existing_backlog_with_order_meeting_requirements(self):
        self.limit_order_agent.order_backlog = {
            'IBM': [{'is_buy_order': True, 'product_id': 'IBM', 'amount': 1000, 'limit': 100}]}
        self.limit_order_agent.handle_order_backlog('IBM', 100)
        self.execution_client.buy.assert_called_once()

    def test_check_existing_backlog_with_order_meeting_requirements_only_called_once(self):
        # should only be called once
        self.limit_order_agent.on_price_tick('IBM', 101)
        self.limit_order_agent.on_price_tick('IBM', 100)
        self.limit_order_agent.on_price_tick('IBM', 99)
        self.limit_order_agent.on_price_tick('IBM', 98)
        self.limit_order_agent.on_price_tick('IBM', 99)
        self.limit_order_agent.on_price_tick('IBM', 100)
        self.execution_client.buy.assert_called_once()

    def test_on_price_tick_IBM_requirements_met(self):
        """Testing the 'happy path', i.e., that the requirements are met for
        1000 shares of IBM to be bought if the price drops below $100."""
        self.limit_order_agent.on_price_tick(product_id="IBM", price=95)
        self.execution_client.buy.assert_called_with("IBM", 1000)

    def test_on_price_tick_IBM_requirements_not_met(self):
        """Testing that a buy is not executed if the requirements are not met,
        i.e., that the requirements are not met for
        1000 shares of IBM to be bought if the price drops below $100."""
        self.limit_order_agent.on_price_tick(product_id="IBM", price=105)
        self.execution_client.buy.assert_not_called()
