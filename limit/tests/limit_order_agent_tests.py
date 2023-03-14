import unittest
from limit.limit_order_agent import \
    (LimitOrderAgent, OrderExecutionClient,
     Order, OrderType, OrderStatus)


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self) -> None:
        self.order_execution_client = OrderExecutionClient()
        self.limit_order_agent = LimitOrderAgent(self.order_execution_client)

    def test_add_order(self):
        self.limit_order_agent.add_order(OrderType.Buy, 'IBM', 1000, 600)
        self.assertIsInstance(self.limit_order_agent.order, Order)

    def test_on_price_tick_sell_order_with_market_above_limit(self):
        product_id = 'IBM'
        price = 900
        self.limit_order_agent.add_order(OrderType.Sell, 'IBM', 1000, 600)
        self.limit_order_agent.on_price_tick(product_id, price)
        self.assertEqual(self.limit_order_agent.order.status, OrderStatus.Sold)

    def test_on_price_tick_buy_order_with_market_below_limit(self):
        product_id = 'IBM'
        price = 300
        self.limit_order_agent.add_order(OrderType.Buy, 'IBM', 1000, 600)
        self.limit_order_agent.on_price_tick(product_id, price)
        self.assertEqual(self.limit_order_agent.order.status, OrderStatus.Bought)

    def test_on_price_tick_buy_order_without_product_id(self):
        product_id = 'APPLE'
        price = 300
        self.limit_order_agent.add_order(OrderType.Buy, 'IBM', 1000, 600)
        self.limit_order_agent.on_price_tick(product_id, price)
        self.assertEqual(self.limit_order_agent.order.status, None)

    def test_on_price_tick_without_buy_order(self):
        product_id = 'IBM'
        price = 300
        self.limit_order_agent.add_order(OrderType.Sell, 'IBM', 1000, 600)
        self.limit_order_agent.on_price_tick(product_id, price)
        self.assertEqual(self.limit_order_agent.order.status, None)

    def test_on_price_tick_without_sell_order(self):
        product_id = 'IBM'
        price = 900
        self.limit_order_agent.add_order(OrderType.Buy, 'IBM', 1000, 600)
        self.limit_order_agent.on_price_tick(product_id, price)
        self.assertEqual(self.limit_order_agent.order.status, None)

    def test_execute_order(self):
        self.limit_order_agent.add_order(OrderType.Sell, 'IBM', 1000, 600)
        self.limit_order_agent.execute_order(OrderType.Buy)
        self.assertEqual(self.limit_order_agent.order.status, OrderStatus.Bought)
        self.limit_order_agent.execute_order(OrderType.Sell)
        self.assertEqual(self.limit_order_agent.order.status, OrderStatus.Sold)


if __name__ == '__main__':
    unittest.main()
