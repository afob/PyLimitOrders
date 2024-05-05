from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class LimitOrder:
    """
    Desc: a limit order with details about the trade.
    Attributes:
        buy_sell_flag (bool): True for buy order, False for sell order.
        product_id (str): The product identifier.
        amount (int): The quantity to buy or sell.
        limit_price (float): The price limit for order execution.
        filled (bool): Indicates whether the order has been filled.
    """
    def __init__(self, buy_sell_flag: bool, product_id: str, amount: int, limit_price: float):
        self.buy_sell_flag = buy_sell_flag
        self.product_id = product_id
        self.amount = amount
        self.limit_price = limit_price
        self.filled = False

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self._execution_client = execution_client
        self._orders = []

    def on_price_tick(self, product_id: str, price: float): 
        """
        Desc: Processes price updates, executing orders if their price limits are met.
        Args:
            product_id (str): The product identifier.
            price (float): The current market price.
        """
        # Check for orders to execute
        for order in self._orders:
            # Logic for matching order type (buy/sell) and price limit
            if (order.buy_sell_flag and price <= order.limit_price) or (not order.buy_sell_flag and price >= order.limit_price):
                try:
                    if order.buy_sell_flag:
                        self._execution_client.buy(order.product_id, order.amount)
                    else:
                        self._execution_client.sell(order.product_id, order.amount)
                    order.filled = True
                except ExecutionException as e:
                    print(f"Order execution failed: {e}")

        # Remove filled orders
        self._orders = [order for order in self._orders if not order.filled]

    def add_order(self, buy_sell_flag: bool, product_id: str, amount: int, limit_price: float):
        """
        Adds a new limit order to the agent's order book.

        Args:
            buy_sell_flag (bool): True for buy, False for sell.
            product_id (str): The product identifier.
            amount (int): The quantity to buy or sell.
            limit_price (float): The limit price for execution.
        """
        self._orders.append(LimitOrder(buy_sell_flag, product_id, amount, limit_price))
