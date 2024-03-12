import unittest

from trading_framework.execution_client import ExecutionClient
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def test_something(self):
        self.fail("not implemented")



    def test_answer1_market_price_less_than_100(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("IBM",99)
        self.assertEqual(limit_order_agent_execute_result, "Buy Order Executed")

 

    def test_answer1_market_price_greater_than_equal_to_100(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("IBM",250)
        self.assertEqual(limit_order_agent_execute_result, "Market price not less than Limit Price")

 

    def test_order_addition_all_valid_arguments(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_add_order_result = limit_order_agent_obj.add_order("BUY","CISCO",5000,350)   
        self.assertEqual(limit_order_agent_add_order_result, "Order Addition succeeded")

 

    def test_order_addition_wrong_buy_sell(self):

        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_add_order_result = limit_order_agent_obj.add_order("WITHDRAW","AXIS",10000,250)    
        self.assertEqual(limit_order_agent_add_order_result, "Order Addition failed as buy or sell not specified / wrongly specified")

 

    def test_order_addition_wrong_amount(self):

        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_add_order_result = limit_order_agent_obj.add_order("SELL","AXIS",-200,250)     
        self.assertEqual(limit_order_agent_add_order_result, "Amount has to be positive")

 

    def test_order_addition_wrong_product_id(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_add_order_result = limit_order_agent_obj.add_order("SELL","",2100,250)        
        self.assertEqual(limit_order_agent_add_order_result, "product_id cannot be null or empty string")

 

    def test_order_addition_wrong_limit(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_add_order_result = limit_order_agent_obj.add_order("SELL","DELL",2100,-100)        
        self.assertEqual(limit_order_agent_add_order_result, "Limit cannot be less than min value 0")

 

    def test_order_execution_buy_limit_reached(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_obj.add_order("SELL","DELL",2100,570)
        limit_order_agent_obj.add_order("BUY","HP",3000,830)
        limit_order_agent_obj.add_order("SELL","AXIS",5000,120)
        limit_order_agent_obj.add_order("BUY","AMUL",2100,780)
        limit_order_agent_obj.add_order("SELL","AMUL",1200,850)
        limit_order_agent_obj.add_order("SELL","IRCTC",4000,900)
        limit_order_agent_obj.add_order("BUY","BHEL",1000,50)        
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("AMUL",700)
        self.assertEqual(limit_order_agent_execute_result, "Buy Order Executed")

 

    def test_order_execution_neither_limits_reached(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_obj.add_order("SELL","DELL",2100,570)
        limit_order_agent_obj.add_order("BUY","HP",3000,830)
        limit_order_agent_obj.add_order("SELL","AXIS",5000,120)
        limit_order_agent_obj.add_order("BUY","AMUL",2100,780)
        limit_order_agent_obj.add_order("SELL","AMUL",1200,850)
        limit_order_agent_obj.add_order("SELL","IRCTC",4000,900)
        limit_order_agent_obj.add_order("BUY","BHEL",1000,50)        
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("AMUL",800)
        self.assertEqual(limit_order_agent_execute_result, "None of the orders are in limit")

 

    def test_order_execution_sell_limit_reached(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_obj.add_order("SELL","DELL",2100,570)
        limit_order_agent_obj.add_order("BUY","HP",3000,830)
        limit_order_agent_obj.add_order("SELL","AXIS",5000,120)
        limit_order_agent_obj.add_order("BUY","AMUL",2100,780)
        limit_order_agent_obj.add_order("SELL","AMUL",1200,850)  
        limit_order_agent_obj.add_order("SELL","IRCTC",4000,900)
        limit_order_agent_obj.add_order("BUY","BHEL",1000,50)        
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("AMUL",900)
        self.assertEqual(limit_order_agent_execute_result, "Sell Order Executed")


    def test_order_execution_order_not_existing(self):
        execution_obj = ExecutionClient()
        limit_order_agent_obj = LimitOrderAgent(execution_obj)
        limit_order_agent_obj.add_order("SELL","DELL",2100,570)
        limit_order_agent_obj.add_order("BUY","HP",3000,830)
        limit_order_agent_obj.add_order("SELL","AXIS",5000,120)
        limit_order_agent_obj.add_order("BUY","AMUL",2100,780)
        limit_order_agent_obj.add_order("SELL","AMUL",1200,850)  
        limit_order_agent_obj.add_order("SELL","IRCTC",4000,900)
        limit_order_agent_obj.add_order("BUY","BHEL",1000,50)        
        limit_order_agent_execute_result = limit_order_agent_obj.on_price_tick("PAYTM",80)
        self.assertEqual(limit_order_agent_execute_result, "None of the orders are in limit")


if __name__ == '__main__':
    unittest.main()
