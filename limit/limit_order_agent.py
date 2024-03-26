from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from flag import FLAG


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()

    def on_price_tick(self, product_id: str):
        # see PriceListener protocol and readme file
        return PriceListener.on_price_tick(product_id)

    def add_order(self, flag : FLAG, product_ids: list, price_limit: float, amount: float):
        if flag == 'Flag.BUY':
            for product_id in product_ids:
                price = LimitOrderAgent.on_price_tick(product_id)
                if price <= price_limit:
                    ExecutionClient.buy(product_id, amount)
        if flag == 'Flag.SELL':
            for product_id in range(len(product_ids)):
                price = LimitOrderAgent.on_price_tick(product_id)
                if price >= price_limit:
                    ExecutionClient.sell(product_id, amount)        

