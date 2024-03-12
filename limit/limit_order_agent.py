from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.order_list = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        
        try:
            ### Part 1 Answer ###
            if(product_id=="IBM" and price<100):
                self.execution_client.buy("IBM",1000)
                return "Buy Order Executed"
            if(product_id=="IBM" and price>=100):
                return "Market price not less than Limit Price"

            ### Part 2 Answer ###
            for order in self.order_list:
                buy_or_sell,ordered_product_id,amount,limit,is_executed = order[0],order[1],order[2],order[3],order[4]
                if(ordered_product_id == product_id and is_executed==0):
                    if(buy_or_sell=="BUY"):
                        if(price<=limit):
                            self.execution_client.buy(ordered_product_id,amount)
                            order[4] = 1  # to show order is executed
                            return "Buy Order Executed"
                    if(buy_or_sell=="SELL"):
                        if(price>=limit):
                            self.execution_client.sell(ordered_product_id,amount)
                            order[4] = 1  # to show order is executed
                            return "Sell Order Executed"
            return "None of the orders are in limit"
        except Exception as e:
            return "Order Execution Failed due to "+str(e)

    def add_order(self,buy_or_sell:str,product_id:str,amount:int,limit:float):
        try:
            # a list or database to store the order
            if(buy_or_sell not in ["BUY","SELL"]):
                return "Order Addition failed as buy or sell not specified / wrongly specified"
            if(amount <=0):
                return "Amount has to be positive"
            if(product_id==None or product_id==""):
                return "product_id cannot be null or empty string"
            if(limit < 0.0):
                return "Limit cannot be less than min value 0"
            self.order_list.append([buy_or_sell,product_id,amount,limit,0])  # last element to determine this order is yet to be executed
            return "Order Addition succeeded"
        except Exception as e:
            return "Order Addition failed due to "+str(e)

### Part 1 Answer ###            
execution_obj = ExecutionClient()
limit_order_agent_obj = LimitOrderAgent(execution_obj)
imit_order_agent_obj.on_price_tick("IBM",99)


### Protocols cannot be instantiated, so there are no values whose runtime type is a protocol ###
### Module (file) names should be ideally same as that of Class Name (case sensitive) ###
