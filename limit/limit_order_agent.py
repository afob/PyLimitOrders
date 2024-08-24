import sys, os
sys.path.append("..")
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class MockExecutionClient(ExecutionClient):
    pass
        
class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.orders = list()
        
       
    def add_order(self, product_id,  operation, amount, price_limit ):
        if operation not in {"buy","sell"}:
            raise ValueError("usage -> operation: 'sell' | 'buy'")
         
            
        if price_limit < 0:
            raise ValueError("price_limit should be greater than zero") 
        
        if amount < 0:
            raise ValueError("Amount should be greater than zero ")
        
        order_dict = {
            "pid": product_id,
            "operation": operation,
            "amount": amount,
            "price_limit": price_limit
        }
          
        self.orders.append((order_dict))   

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        pop_order=[]
        order_list=self.orders
        for order in order_list:
            pd_id = order["pid"]
            operation = order["operation"]
            amount = order["amount"]
            price_limit = order["price_limit"]
            try:
                if product_id == pd_id:
                    if operation == "buy" and price <= price_limit: # Buy if price  is less than  price_limit
                        self.execution_client.buy(pd_id,amount)  
                        pop_order.append(order) # add value into pop_order  
                    elif operation == "sell" and price >= price_limit: # sell if price is greater than price_limit
                        self.execution_client.sell(pd_id, amount)
                        pop_order.append(order)# add value into pop_order
            except Exception as err:
                print(err)
                    
        for order in pop_order:
            self.orders.remove(order)          

                
                

if __name__ == "__main__":
    exe_obj = MockExecutionClient()
    order_obj = LimitOrderAgent(exe_obj)
    order_obj.add_order("prod_1","buy", 500,100)
    order_obj.add_order("prod_2","buy", 1000,10)
    order_obj.add_order("prod_3","sell", 950,150)
    print("order list")
    print(order_obj.orders)
    order_obj.on_price_tick("prod_1",90) ##should execute buy operation
    order_obj.on_price_tick("prod_2",90) ##Should not execute buy operation
    order_obj.on_price_tick("prod_3",200) ##Should execute sell operation
    print("order list after price_tick")
    print(order_obj.orders)
    
    
    
    
     
        
        
    


