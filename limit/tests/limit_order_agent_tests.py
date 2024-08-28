import unittest

from limit.limit_order_agent import LimitOrderAgent
class MockExecutionClient:
    def __init__(self) -> None:
        self.executed_order = []
    
    def buy(self,order_type, amt):
        self.executed_order.append((order_type, amt, 'buy'))
    
    def sell(self,order_type, amt):
        self.executed_order.append((order_type, amt, 'sell'))
class Test(unittest.TestCase):
    client = MockExecutionClient()
    def test_buy(self):
        #adding order
        print(1)
        agent = LimitOrderAgent(self.client)
        agent.add_order('buy', 'IBM', 1000, 100)
        agent.on_price_tick('IBM', 99)
        self.assertIn(('IBM', 1000, 'buy'), self.client.executed_order)
        self.assertEqual(len(agent.orders), 0)
    
    def test_sell(self):
        print(2)
        agent = LimitOrderAgent(self.client)
        agent.add_order('sell', 'IBM', 500, 150)
        agent.on_price_tick('IBM', 151)
        self.assertIn(('IBM', 500, 'sell'), self.client.executed_order)
        self.assertEqual(len(agent.orders), 0)

    def test_buy_negative(self):
        #adding order
        agent = LimitOrderAgent(self.client)
        agent.add_order('buy', 'APPL', 1000, 100)
        agent.on_price_tick('APPL', 101)
        self.assertNotIn(('APPL', 1000, 'buy'), self.client.executed_order)
        self.assertEqual(len(agent.orders), 1)
    
    def test_sell_negative(self):
        agent = LimitOrderAgent(self.client)
        agent.add_order('sell', 'GOOGL', 500, 150)
        agent.on_price_tick('GOOGL', 110)
        self.assertNotIn(('GOOGL', 500, 'sell'), self.client.executed_order)
        self.assertEqual(len(agent.orders), 1)

if __name__ == "__main__":
    unittest.main()
    