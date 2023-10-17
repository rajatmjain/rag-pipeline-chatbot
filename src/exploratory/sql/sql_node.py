import os
import pandas as pd
import sqlite3
from haystack.nodes import PromptNode,PromptTemplate,AnswerParser
from haystack.document_stores import SQLDocumentStore
from haystack.pipelines import Pipeline
from haystack import Document

class SQLNode:

    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")

    def documentStore(self):
        documentStore = SQLDocumentStore(url="sqlite:///data/database.db")
        conn = sqlite3.connect("data/database.db")
        df = pd.read_sql_query("SELECT * from gold_prices",conn)

        docs = [
            Document(content=df,
                    content_type="table",
                    meta={}),
                ]

        documentStore.write_documents(documents=docs)

        return documentStore
    
    def pipeline(self):
        # Prompt Template
        promptTemplate = PromptTemplate(prompt = 
                               """" You are an assistant getting data of prices of gold from documents. The table has the columns Date,Open,High,Low,Close,Volume. The dates are in the format "%Y-%m-%d" example: October 9 2023 is 2023-10-09.
                                Strictly answer the following query briefly based on the provided data from the documents and nothing else.
                                If the context does not include an answer, reply with 'The data does not contain information related to the question'.\n
                                Query: {query}\n
                                Documents: {documents}\n
                                Answer: 
                                """,
                                output_parser=AnswerParser())

        # Prompt Node initialization
        promptNode = PromptNode(self.hfModelName,api_key=self.hfAPIKey,default_prompt_template=promptTemplate)

        # Pipeline
        sqlPipeline = Pipeline()

        # Add Nodes to sqlPipeline
        sqlPipeline.add_node(component=promptNode, name="PromptNode", inputs=["Query"])

        return sqlPipeline