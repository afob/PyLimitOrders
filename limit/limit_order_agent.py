from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_method = execution_client
        self.order_products = [] 
        self.status = ""      

    def execute_orders(self, product_id: str, price: float) -> None:
        """
        Execute any held orders when the market price is at or better than the limit
        :param product_id: ID of the product
        :param price: Current market price
        """

        for order in self.order_products:
            is_buy, prod_id, amount, limit = order
            print(order)
            if prod_id == product_id:
                print(prod_id, is_buy)
                try:
                    if is_buy == True:
                        print(is_buy)
                        if price < limit:
                            try:
                                self.execution_method.buy(self,prod_id, amount)
                                self.status = "Brought"
                                print("here")
                                #To run the exception test cases , uncomment the below line
                                #raise ExecutionException("Exception raised during buying the share")

                            except ExecutionException as e:
                                print(f"Failed to buy an order for prod_id {product_id}:{e}")
                                self.status = "Failed to buy"
                        else:
                            self.status = "Hold"
                    elif is_buy == False and price >= limit:
                        print(limit, price)
                        try:
                            self.execution_method.sell(self,prod_id, amount)
                            self.status = "Sold"
                            self.order_products.remove(order)

                            #To run the exception test cases , uncomment the below line
                            #raise ExecutionException("Exception raised during selling the share")
                        except ExecutionException as e:
                            print(f"Failed to sell an order for prod_id {product_id}:{e}")
                            self.status = "Failed to sell"
                        
                except ExecutionException as e:
                    print(f"Failed to execute order: {e}")


    def on_price_tick(self, product_id: str, price: float) -> None:
        """
        Invoked on market data change
        :param product_id: ID of the product that has a price change
        :param price: The current market price of the product
        """
        self.execute_orders(product_id, price)
    def add_order(self, is_buy: bool, product_id: str, amount: int, limit: float) -> None:
        """
        Add an order to the list of pending orders
        :param buy: True if is_buy order, False if sell order
        :param product_id: ID of the product
        :param amount: Amount to buy/sell
        :param limit: Price limit for the order
        """
        self.order_products.append((is_buy, product_id, amount, limit))

