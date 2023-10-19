import os
from haystack.agents import Agent
from haystack.agents.base import ToolsManager
from haystack.nodes import PromptTemplate,PromptNode
from goldNews.newstool import NewsTool
from goldPrices.pricestool import PricesTool


class GoldBotAgent:
    
    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")
        
    def agent(self) -> Agent:

        agentPrompt = """
                        In the following conversation, a human user interacts with an AI Agent. The human user poses questions, and the AI Agent goes through several steps to provide well-informed answers.
                        The AI Agent must use the available tools to find the up-to-date information. The final answer to the question should be truthfully based solely on the output of the tools. The AI Agent should ignore its knowledge when answering the questions.
                        The AI Agent has access to these tools:
                        {tool_names_with_descriptions}

                        AI Agent responses must start with one of the following:

                        Thought: [the AI Agent's reasoning process]
                        Tool: [tool names] (on a new line) Tool Input: [input as a question for the selected tool WITHOUT quotation marks and on a new line] (These must always be provided together and on separate lines.)
                        Observation: [tool's result]
                        Final Answer: [final answer to the human user's question]
                        When selecting a tool, the AI Agent must provide both the "Tool:" and "Tool Input:" pair in the same response, but on separate lines.

                        The AI Agent should not ask the human user for additional information, clarification, or context.
                        If the AI Agent cannot find a specific answer after exhausting available tools and approaches, it answers with Final Answer: inconclusive

                        Question: {query}
                        Thought:
                        {transcript}
                        """

        promptTemplate = PromptTemplate(
            prompt= agentPrompt
            )
        
        promptNode = PromptNode(model_name_or_path=self.hfModelName,api_key=self.hfAPIKey)

        pricesTool = PricesTool.tool()
        newsTool = NewsTool.tool()

        goldBotAgent = Agent(
            prompt_node=promptNode,
            prompt_template=promptTemplate,
            prompt_parameters_resolver=self.resolverFunction,
            tools_manager= ToolsManager(tools=[pricesTool,newsTool])
        )

        return goldBotAgent

    def resolverFunction(self,query, agent, agent_step):
        return {
            "query": query,
            "tool_names_with_descriptions": agent.tm.get_tool_names_with_descriptions(),
            "transcript": agent_step.transcript,
        }


agent = GoldBotAgent().agent().run(query="Summarize news on gold")

print(agent)