from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.orders = []  
        self.market_price=100      
        super().__init__()

    def add_order(self, order_type: str, product_id: str, price: float, limit: int):
        if order_type == "BUY" or order_type == "SELL":
            self.orders.append({'flag' : order_type , 'Product_id':product_id , 'amount':price , 'limit' : limit})

    def execute_order(self):
        for order in self.orders:
            if self.market_price < order.amount and order.flag=="BUY":
                self.execution_client.buy(order.Product_id , order.amount) 
                self.on_price_tick(order.Product_id , order.amount)
            elif self.market_price >= order.amount and order.flag=="SELL":
                self.execution_client.sell(order.Product_id , order.amount)    
                self.on_price_tick(order.Product_id , order.amount)

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        pass


