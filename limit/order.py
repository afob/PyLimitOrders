from datetime import datetime
from uuid import uuid4
from limit.flag import Flag


class Order:

    def __init__(self, flag: Flag, product_id: str, amount: int, limit: float) -> None:
        """
        An order for a security

        :param flag: buy or sell
        :param product_id: ticker
        :param amount: amount to buy
        :param limit: price for limit order
        """

        super().__init__()
        self.flag = flag
        self.product_id = product_id
        self.amount = amount
        self.limit = limit
        self.id = str(uuid4())
        self.time_created = datetime.now()
        # TODO: Add validation for parameters
