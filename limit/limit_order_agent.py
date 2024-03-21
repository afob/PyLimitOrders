from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener





class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if(price < 100):
            self.execution_client.buy(Product_id ,1000)
            
        return True
