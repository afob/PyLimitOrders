# LimitOrders

The task is to implement a simple limit order system utilising the protocols provided by the trading framework. 
You can assume that in a live environment your LimitOrderAgent class would be provided with market data via the
price_tick method and would be able to execute orders via an ExecutionClient instance given to it in the constructor.

## The trading_framework model
The **trading_framework** module is provided and cannot be modified.
It has some limitations and flaws, feel free to point them out as you implement your solution.

### Limitations
    * No partial order fill support
    * No support for special types (fill or kill, time limit, etc)
    * No way to check against user balance, pattern day trade, etc

## Tests
Provide tests to prove that your code is working. This is especially important since no working implementation of
the trading framework is provided.

### User Stories
* As a user, I want to create orders, so that the agent is aware of what orders to execute
* As a user, I want to specify the order parameters, so the agent can execute them conditionally
    * Parameters:
        * Order flag (Buy, Sell)
        * Product ID
        * Amount to Buy or Sell
        * Limit at which to buy or sell

## Guidance
### In the **limit.limit_order_agent** module only:
1. Implement LimitOrderAgent such that it buys 1000 shares of IBM when the price drops below $100

2. Extend LimitOrderAgent such that it:
   * accepts orders through an add_order method, that accepts the following parameters
     * a flag indicating whether to buy or sell
     * a product id
     * an amount to buy/sell
     * the limit at which to buy or sell  
   * executes any held orders when the market price is at or better than the limit 


