from abc import ABC, abstractmethod

class PriceListener(ABC):

    @abstractmethod
    def on_price_tick(self, product_id: str, price: float):
        """
        :param product_id: The product for which the price update is received.
        :param price: The current price of the product.
        """
        pass

