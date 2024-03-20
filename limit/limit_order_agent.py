from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
from collections import deque


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client=execution_client
        self.orders=deque()

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        try:
            if product_id=='IBM' and price<100:
                self.execution_client.buy(product_id,1000)
        except ExecutionException:
            raise "Price greater than $100, unable to process"

        for i in range(len(self.orders)):
            ord_typ,ord_price,p_id,amount=self.orders.popleft()
            if p_id==product_id and (ord_typ=='buy' and ord_price<100) or (ord_typ=='sell' and ord_price>=100):
                try:
                    if ord_typ=='buy':
                        self.execution_client.buy(p_id,amount=amount)
                    self.execution_client.sell(p_id,amount=amount)
                except ExecutionException:
                    raise "Not availble"
    def add_orders(self,ord_typ: str, ord_price: float, p_id: str,amount: float):
        self.orders.append((ord_typ,ord_price,p_id,amount))




