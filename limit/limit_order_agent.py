from execution_client import ExecutionClient
from price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client=execution_client
        self.all_orders=[]

    def on_price_tick(self, product_id: str, mkt_price: float):
        for order in self.all_orders:
            print()
            print(f"Market Price: {mkt_price}")
            print(f"Set price limit of user: {order['limit']}")
            if order["buy"] and order['product_id'] == product_id and order['limit'] >= mkt_price:
                #buy
                self.execute_order(order)
                
            elif order['product_id'] == product_id and order['limit'] <= mkt_price:
                #will sell all orders if there any if mkt price is higher than limit
                print(f"Not buying orders as market price is high- {mkt_price} then set limit {order['limit']} instead selling them")
                order["buy"]=False
                self.execute_order(order)
                #self.all_orders.remove(order)

    def add_order(self, buy_or_sell: bool, product_id: str, total_shares: int, limit_to_buy_sell: float):
        if buy_or_sell:
            self.all_orders.append({'buy': True, 'product_id': product_id, 'total_shares': total_shares, 'limit': limit_to_buy_sell})
        else:
            self.all_orders.append({'buy': False, 'product_id': product_id, 'total_shares': total_shares, 'limit': limit_to_buy_sell})


    def execute_order(self, order):
        if order["buy"]:
            self.execution_client.buy(order['product_id'], order['total_shares'])
        else:
            self.execution_client.sell(order['product_id'], order['total_shares'])
        self.all_orders.remove(order)

