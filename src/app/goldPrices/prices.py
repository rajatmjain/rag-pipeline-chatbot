from goldPrices.pricesnode import PricesNode

class Prices:

    def __init__(self) -> None:
        pass

    def node(self) -> PricesNode:
        return PricesNode(db_path="data/database.db")