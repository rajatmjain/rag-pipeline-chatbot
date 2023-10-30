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
