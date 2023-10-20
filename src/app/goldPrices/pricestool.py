from haystack.agents import Tool
from goldPrices.pricesnode import PricesNode
from goldPrices.prices import Prices

class PricesTool():
    def __init__(self) -> None:
        pass

    def tool() -> Tool:
        prices = Prices()
        pricesDocumentStore = PricesNode().documentStore()
        pricesPipeline = prices.pipeline()
        pricesTool = Tool(
            name="PricesTool",
            description="This is a tool to provide real time gold prices and quantitative analysis on gold prices.",
            pipeline_or_node=pricesPipeline,
            output_variable="result", 
        )
        return pricesTool