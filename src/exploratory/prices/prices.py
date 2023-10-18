from prices_node import PricesNode
from haystack.pipelines import Pipeline

class Prices:

    def __init__(self) -> None:
        pass

    def pipeline(self) -> Pipeline:
        return PricesNode().pipeline()