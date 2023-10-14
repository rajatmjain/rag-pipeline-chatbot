import os
import sqlite3
from haystack.nodes import PromptNode, PromptTemplate
import pandas as pd

class SQLQueryGenerator():

    def __init__(self):
        # Model configurations
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")


    def generateSQL(self,query:str):

        columns = self.getTableColumns()

        sqlPrompt = PromptTemplate(prompt="""Please generate an SQL query. The query should answer the following Query: {query};
                                                              The query is to be answered for the table is called 'historic_prices' with the following
                                                              Columns: {columns} ;
                                                              Answer:""",
                            )

        promptNode = PromptNode(self.hfModelName,api_key=self.hfAPIKey,default_prompt_template=sqlPrompt)

        output = promptNode.prompt(prompt_template=sqlPrompt,query=query,columns=columns)

        return output[0]
    
    def getTableColumns(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('data/historic_prices.db')

        # Use Pandas to read the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM historic_prices LIMIT 1", conn)

        # Get column names as a comma-separated string
        columnNames = ','.join(df.columns)

        # Close the database connection
        conn.close()

        return columnNames