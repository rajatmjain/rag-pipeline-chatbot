import os
from haystack.agents import Agent
from haystack.agents.base import ToolsManager
from haystack.nodes import PromptTemplate,PromptNode
from src.exploratory.news.news_tool import NewsTool
from src.exploratory.prices.prices_tool import PricesTool


class GoldBotAgent:
    
    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")
        
    def agent(self) -> Agent:

        promptTemplate = PromptTemplate(
            prompt= """

            """
            )
        
        promptNode = PromptNode(model_name_or_path=self.hfModelName,api_key=self.hfAPIKey)

        pricesTool = PricesTool.tool()
        newsTool = NewsTool().tool()

        goldBotAgent = Agent(
            prompt_node=promptNode,
            prompt_template=promptTemplate,
            tools_manager= ToolsManager(tools=[pricesTool,newsTool])
        )

        return goldBotAgent

