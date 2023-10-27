import os
import pandas as pd
import sqlite3
from haystack.nodes import PromptNode,PromptTemplate
from sympy import true
from dotenv import load_dotenv
from haystack.nodes.base import BaseComponent
from haystack.agents import Agent, Tool
load_dotenv()

class PricesNode(BaseComponent):
    outgoing_edges = 1

    def __init__(self,db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
    
    def run(self, query: str):
        try:
            df = pd.read_sql_query(query, self.conn)
            output = {
                "results": f"{df}",
                "query": query,
            }
            return output
        except Exception as e:
            output = {
                "results": str(e),
                "query": query,
            }
            return output
        
    
    def run_batch(self):
         pass
    
class PriceAgent():
    def __init__(self):
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")

    def agent(self) -> Agent:
        # Prompt Template
        sql_agent_prompt = PromptTemplate(
            prompt="You are a helpful and knowledgeable agent who has access to an SQL database which has a table called 'gold_prices'"
                        " that has the following Columns: Date;Open;High;Low;Close;Volume"
                        "Your task is to assess whether a query can be resolved with the tools you have at hand, and if yes, generate an SQL query to resolve it."
                        "The generated SQL query should be stripped down to just the query with no syntax highlighting."
                        "You have access to the following tools:\n\n"
                        "{tool_names_with_descriptions}\n\n"
                        "To answer questions, you'll need to go through multiple steps involving step-by-step thinking and "
                        "selecting appropriate tools and their inputs; tools will respond with observations."
                        "When you are ready with an answer, respond with the `Final Answer:`\n\n"
                        "If the query is unrelated and cannot be answered by any of the tools, your final answer should say 'Cannot be answered with available databases'\n\n"
                        "Use the following format:\n\n"
                        "Question: the question to be answered\n"
                        "Thought: Reason if you have the final answer. If yes, answer the query. If not, continue using the tools to resolve the query.\n"
                        "Tool: pick one of {tool_names} \n"
                        "Tool Input: the input for the tool.\n"
                        "Observation: The full result the tool responds with\n"
                        "...\n"
                        "Final Answer: the final answer to the query. This should be the full result of the SQL query that you came up with.\n\n"
                        "Thought, Tool, Tool Input, and Observation steps can be repeated multiple times, but sometimes we can find an answer in the first pass\n"
                        "---\n\n"
                        "Question: {query}\n"
                        "Thought: Let's think step-by-step, I first need to\n"
                        "{transcript}",
        )

        prompt_node = PromptNode(model_name_or_path=self.hfModelName, api_key=self.hfAPIKey, stop_words=["Observation:"], max_length=1000)
        agent = Agent(prompt_node=prompt_node, prompt_template=sql_agent_prompt)
        return agent


query_node = PricesNode(db_path="data/database.db")
agent = PriceAgent().agent()
sql_query_tool =  Tool(name="SQLQuery", pipeline_or_node=query_node, description="""This tool is useful for consuming SQL queries and responds with the result""")
agent.add_tool(sql_query_tool)
agent.run("What was the opening price of gold on October 26, 2023")
