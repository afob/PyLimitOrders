from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.orders=[]
        self.execution_client = execution_client
        
    def add_order(self,buy:bool,product_id:str,amount:int,price_limit:float):
        """
        order's to be added
        :param by: a flag to indicate whether to buy or sell
        :param product: ID of the product
        :param amount: amount to buy/sell
        :price limit: price limit of product to buy/sell
        """
        try:
        
            order_dict={"is_buy":buy,"prod_id":product_id,"price":amount,"price_limit":price_limit}
            self.orders.append(order_dict)
            
        except Exception as e:
        
            print(f"Exception at add_order : {e}")

    def on_price_tick(self, product_id: str, price: float):
        """
        Called whenever we need to updat price for the product.
        :param product_id: PRODUCT ID
        :param price: Price of the product
        """
        try:
        
            for order in list(self.orders):
                
                if order["prod_id"] == product_id:
                
                    if order["is_buy"] and price<=order["price_limit"]:
                    
                        self.execution_client.buy(product_id,order["price"])
                        self.orders.remove(order)
                        
                    elif (not order["is_buy"]) and price>=order["price_limit"]:
                    
                        self.execution_client.buy(product_id,order["sell"])
                        self.orders.remove(order)
                        
        except Exception as e:
        
            print(f"Exception at on_price_tick : {e}")