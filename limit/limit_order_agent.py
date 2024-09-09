from trading_framework.execution_client import ExecutionClient,ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):


    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client=execution_client
        self.orders=[]

    def add_orders(self, is_buy:bool,product_id:str,amount:int,price_limit:float):
        """
        Adding orders
            :param is_buy: a flag indicating whether to buy or sell
            :param product: A product ID
            :param amount: An amount to buy/sell
            :price limit: The limit at which to buy/sell
        """
        try:
            orders_list = {
                'is_buy': is_buy,
                'product_id': product_id,
                'amount': amount,
                'price_limit': price_limit
            }
        except Exception as e:
            print(f"Exception at add_orders : {e}")
        else:
            self.orders.append(orders_list)
        
        
    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        """
        For updation of the buy and sell orders
        :param product_id: product id of the order
        :param price: product price
        """
        try:
            for order in list(self.orders):
                if order["product_id"] == product_id:
                
                    if order["is_buy"] and (price<=order["price_limit"]):
                        self.execution_client.buy(product_id,order["amount"])
                        self.orders.remove(order)
                        return True
                        
                    elif (not order["is_buy"]) and (price>=order["price_limit"]):
                    
                        self.execution_client.sell(product_id,order["amount"])
                        self.orders.remove(order)
                        return True
                        
            return False
                # else:
                #     raise ExecutionException
                    
        except Exception as e:
            print(f"Exception at on_price_tick : {e}")


