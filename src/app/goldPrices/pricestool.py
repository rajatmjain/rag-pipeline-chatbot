from haystack.agents import Tool
from goldPrices.pricesnode import PricesNode
from goldPrices.prices import Prices

class PricesTool():
    def __init__(self) -> None:
        pass

    def tool(self) -> Tool:
        prices = Prices()
        pricesNode = prices.node()
        pricesTool = Tool(name="PricesTool", 
                          pipeline_or_node=pricesNode, 
                          description="""This tool is useful for consuming SQL queries and responds with the result. This tool has access to who has access to an SQL database which has a table called 'gold_prices'
                        that has the following Columns: Date;Open;High;Low;Close;Volume """) 
        
        return pricesTool