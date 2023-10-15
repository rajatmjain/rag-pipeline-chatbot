import os
import sqlite3
from haystack.nodes import PromptNode, PromptTemplate
import pandas as pd

class SQLQueryGenerator():

    def __init__(self):
        # Model configurations
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")


    def generateSQL(self,query:str) -> str:

        columns = self.getTableColumns()

        sqlPrompt = PromptTemplate(prompt="""Please generate and return only an SQL query. The query should answer the following Query: {query};
                                                              The query is to be answered for the table is called 'gold_prices' with the following
                                                              Columns: {columns} ;
                                                              Answer:""",
                            )

        promptNode = PromptNode(self.hfModelName,api_key=self.hfAPIKey,default_prompt_template=sqlPrompt)

        output = promptNode.prompt(prompt_template=sqlPrompt,query=query,columns=columns)

        return output[0].strip()
    
    def getTableColumns(self) -> str:
        # Connect to the SQLite database
        conn = sqlite3.connect('data/database.db')

        # Use Pandas to read the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM gold_prices LIMIT 1", conn)

        # Get column names as a comma-separated string
        columnNames = ','.join(df.columns)

        # Close the database connection
        conn.close()

        return columnNames

