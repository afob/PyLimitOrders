from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class ExecutionClientSample:
    """this class object implements 
    the Protocol created by ExecutionClient
    """
    def buy(self, Product_id : str ,amount : int):
        """ here will be code to buy """
        pass 
        
    def sell(self, Product_id : str ,amount : int):
        """ here will be code to sell """
        pass
 
class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.added_orders = []
        
    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        # buy Product 1000 share if price is below 100
        #Part 1
        
        if(price < 100 and product_id == 'IBM'):
            self.execution_client.buy(Product_id , 1000)
            return True   
            
        #part 2
        for order_data in self.added_orders:
            if(order_data['flag'] == 'B' and order_data['product_id']== product_id and order_data['limit'] >= price):
                self.execution_client.buy(Product_id , order_data['amount'])
               
                self.added_orders.remove(order_data)
                 
                
            elif(order_data['flag'] == 'S' and order_data['product_id']== product_id and order_data['limit'] <= price):
                self.execution_client.sell(Product_id , order_data['amount'])
                
                self.added_orders.remove(order_data)
                
        return True

    
    def add_order(self, flag : str, Product_id: str, amount :int, limit : int):
        # based on the flag buy or sell added orders
        
        if(flag == 'B' or flag == 'S'):
            self.added_orders.append({'flag' : flag , 'Product_id'=Product_id , 'amount'=amount , 'limit' = limit})            
            return True
        


