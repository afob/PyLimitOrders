import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


BUY = True
SELL = False

class LimitOrderAgentTest(unittest.TestCase):

    def test_add_order(self):
        def test_buy_on_price_tick(self):
            execution_client_obj = ExecutionClient()
            limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

            res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
            self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

    def test_buy_on_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 100, 'amount': 500, 'operation': BUY})


    def test_sell_on_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(SELL, "IBM", 300, 150)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 160)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 150, 'amount': 300, 'operation': SELL})

    def test_no_action_on_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 120, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 101)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        self.assertNotIn('IBM', limit_order_agent_obj.completed_orders.keys())

    def test_buy_on_first_price_tick_only(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1],
                         {'limit': 100, 'amount': 500, 'operation': BUY})

        completed_orders_count = len(limit_order_agent_obj.completed_orders['IBM'])

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 98)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(len(limit_order_agent_obj.completed_orders['IBM']),
                         completed_orders_count)
    def test_sell_on_first_price_tick_only(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(SELL, "IBM", 300, 150)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 160)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 150, 'amount': 300, 'operation': SELL})

        completed_orders_count = len(limit_order_agent_obj.completed_orders['IBM'])

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 98)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(len(limit_order_agent_obj.completed_orders['IBM']),
                         completed_orders_count)

    def test_buy_multiple_product_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        res = limit_order_agent_obj.add_order(BUY, "TCS", 600, 200)
        self.assertEqual(len(limit_order_agent_obj.orders['TCS']), 1)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 100, 'amount': 500, 'operation': BUY})

        price_tick_result = limit_order_agent_obj.on_price_tick("TCS", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['TCS']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['TCS'][-1], {'limit': 200, 'amount': 600, 'operation': BUY})

    def test_buy_and_sell_product_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        res = limit_order_agent_obj.add_order(SELL, "IBM", 300, 150)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 2)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 100, 'amount': 500, 'operation': BUY})

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 160)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 150, 'amount': 300, 'operation': SELL})


    def test_multiple_limit_buy_and_sell_product_price_tick(self):
        execution_client_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_client_obj)

        res = limit_order_agent_obj.add_order(BUY, "IBM", 500, 100)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        res = limit_order_agent_obj.add_order(BUY, "IBM", 1000, 80)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 2)
        res = limit_order_agent_obj.add_order(SELL, "IBM", 300, 150)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 3)
        res = limit_order_agent_obj.add_order(SELL, "IBM", 500, 180)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 4)

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 99)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 3)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 100, 'amount': 500, 'operation': BUY})


        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 160)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 2)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 150, 'amount': 300, 'operation': SELL})

        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 79)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 1)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 80, 'amount': 1000, 'operation': BUY})


        price_tick_result = limit_order_agent_obj.on_price_tick("IBM", 190)
        self.assertEqual(len(limit_order_agent_obj.orders['IBM']), 0)
        self.assertEqual(limit_order_agent_obj.completed_orders['IBM'][-1], {'limit': 180, 'amount': 500, 'operation': SELL})
