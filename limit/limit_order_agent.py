from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class ExecutionClientSample:
    def buy(self, Product_id : str ,amount : int):
        # code to buy share 
        pass
        
    def sell(self, Product_id : str ,amount : int):
        # code to sell share
        pass
        
class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
  
    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if(price < 100):
            self.execution_client.buy(Product_id ,1000)
            
        return True
        
    def add_order(self, flag : str, Product_id: str, amount :int, limit : float):
        """ Based on flag this function use buy or sell function , limit paramter not understood hence not used """
        if(flag == 'B'):
            self.execution_client.buy(Product_id ,amount)
            return True
        elif(flag == 'S'):
            self.execution_client.sell(Product_id ,amount)
            return True

