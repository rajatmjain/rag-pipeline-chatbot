import os
from haystack.agents import Agent
from haystack.agents.base import ToolsManager
from haystack.nodes import PromptTemplate,PromptNode
from src.exploratory.sql.sql_tool import SQLTool

class GoldBot:
    
    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")
        

    def agent(self):

        promptTemplate = PromptTemplate(
            prompt= """

            """
            )
        
        promptNode = PromptNode(model_name_or_path=self.hfModelName,api_key=self.hfAPIKey)

        sqlTool = SQLTool().tool()

        goldBotAgent = Agent(
            prompt_node=promptNode,
            prompt_template=promptTemplate,
            tools_manager= ToolsManager(tools=[sqlTool])
        )