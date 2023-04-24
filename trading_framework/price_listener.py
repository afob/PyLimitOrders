from typing import Protocol


class PriceListener(Protocol):

    def on_price_tick(self, product_id: str, price: float):
        """
        invoked on market data change
        :param product_id: id of the product that has a price change
        :param price: the current market price of hte product
        :return: None
        """
        ...
