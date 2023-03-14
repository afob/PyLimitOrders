from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import random


# ================Order Entity =====================================
class OrderType(Enum):
    Buy = 'BUY'
    Sell = 'SELL'


class OrderStatus(Enum):
    Bought = 'BOUGHT'
    Sold = 'SOLD'


@dataclass
class Order:
    product: str
    amount: float
    limit: float
    order_type: str
    status: str = None


# =================Static Data==========================

ORDER_POOL = defaultdict(list)
ORDERED_POOL = defaultdict(list)

products = ['IBM', 'APP', 'MIC', 'AMZ', 'VOD', 'ORA']
MarketData = {p: 100 for p in products}

stocks = [('IBM', 1000, 600, OrderType.Buy),
          ('APP', 800, 400, OrderType.Buy),
          ('VOD', 600, 600, OrderType.Sell),
          ('IBM', 400, 300, OrderType.Sell),
          ('MIC', 1000, 500, OrderType.Buy),
          ('APP', 400, 500, OrderType.Sell),
          ('VOD', 400, 500, OrderType.Buy),
          ('APP', 200, 600, OrderType.Sell),
          ('APP', 200, 700, OrderType.Sell),
          ('ORA', 400, 500, OrderType.Buy),
          ('IBM', 1200, 500, OrderType.Buy),
          ('MIC', 16000, 500, OrderType.Sell),
          ('IBM', 1000, 600, OrderType.Buy),
          ('APP', 800, 400, OrderType.Buy),
          ('VOD', 600, 600, OrderType.Sell),
          ('IBM', 400, 300, OrderType.Sell),
          ]

orders = [Order(*d) for d in stocks]
for order in orders:
    ORDER_POOL[order.product].append(order)


# =======Ticker Generator that simulates the Price Ticking to change Market Data====

def ticker_generator():
    product = random.choice(products)
    price = random.randint(30, 1000)
    MarketData[product] = price
    yield product, price


# ======================Execute Order  [BUY | SELL ]===========================================
def execute(order, ordertype):
    if ordertype == OrderType.Buy:
        order.status = OrderStatus.Bought
    elif ordertype == OrderType.Sell:
        order.status = OrderStatus.Sold
    print('Executed Order: ', order)
    ORDERED_POOL[order.product].append(order)
    ORDER_POOL[order.product].remove(order)
    return


# =====================On price Change Event ====================================================
def on_price_change(product, price):
    print('Market Data: ', product, price)

    orders = ORDER_POOL[product] if product in ORDER_POOL else None

    if orders:
        for order in orders:
            if (order.order_type == OrderType.Buy) and (order.limit >= price) and (not order.status):
                execute(order, OrderType.Buy)
            elif (order.order_type == OrderType.Sell) and (order.limit <= price) and (not order.status):
                execute(order, OrderType.Sell)
            else:
                pass


def check_what_happened():
    print('-----------ORDER POOL------------')
    for product, orders in ORDER_POOL.items():
        print(product)
        print(orders)
    print('-----------ORDERED POOL------------')
    for product, orders in ORDERED_POOL.items():
        print(product)
        print(orders)


def main(apply_ticks):
    for _ in range(apply_ticks):
        price_change = ticker_generator()
        product, price = next(price_change)
        on_price_change(product, price)
    check_what_happened()


if __name__ == '__main__':
    APPLY_TICKS = 1
    main(APPLY_TICKS)
