from limit.limit_order_agent import LimitOrderAgent


class MockExecutionClient:
    def __init__(self):
        self.executed_orders = []

    
    def buy(self, product_id: str, amount: int):
        self.executed_orders.append((product_id, amount, 'buy'))

    def sell(self, product_id: str, amount: int):
        self.executed_orders.append((product_id, amount, 'sell'))

def test_limit_order_agent():
    execution_client = MockExecutionClient()
    agent = LimitOrderAgent(execution_client)

    # Test 1: Buy 1000 shares of tata when the price drops below $100
    agent.add_order('buy', 'tata', 1000, 100)
    agent.on_price_tick('tata', 99)
    assert ('tata', 1000, 'buy') in execution_client.executed_orders
    assert len(agent.orders) == 0  # Order should be removed after execution

    # Test 2: Sell 500 shares of tata when the price rises above $150
    agent.add_order('sell', 'tata', 500, 150)
    agent.on_price_tick('tata', 151)
    assert ('tata', 500, 'sell') in execution_client.executed_orders
    assert len(agent.orders) == 0  # Order should be removed after execution

    # Test 3: Buy 200 shares of ph when the price drops below $120
    agent.add_order('buy', 'ph', 200, 120)
    agent.on_price_tick('ph', 121)
    assert ('ph', 200, 'buy') not in execution_client.executed_orders  # Order should not execute
    assert len(agent.orders) == 1  # Order should still be present

    print("All tests passed!")

# Run the tests
if __name__ == "__main__":
    test_limit_order_agent()