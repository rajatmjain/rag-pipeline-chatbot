import os
import pandas as pd
import sqlite3
from haystack.nodes import PromptNode,PromptTemplate,AnswerParser,TfidfRetriever, TableTextRetriever
from haystack.document_stores import SQLDocumentStore
from haystack.pipelines import Pipeline
from haystack import Document

class PricesNode:

    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")

    def documentStore(self) -> SQLDocumentStore:
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
    
    # def retriever(self) -> TfidfRetriever:
    #     tfidfRetriever = TfidfRetriever(
    #         document_store=self.documentStore(),
    #         top_k=5,
    #         auto_fit=True
    #     )
    #     TableTextRetriever()
    #     return tfidfRetriever
    
    def pipeline(self) -> Pipeline:
        # Prompt Template
        promptTemplate = PromptTemplate(prompt = 
                               """" You are a pipeline for getting data of prices of gold from documents. The table has the columns Date,Open,High,Low,Close,Volume. The dates are in the format "%Y-%m-%d" example: October 9 2023 is 2023-10-09.
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
        pricesPipeline = Pipeline()

        # Add Nodes to sqlPipeline
        pricesPipeline.add_node(component=self.retriever(),name="Retriever",inputs=["Query"])
        pricesPipeline.add_node(component=promptNode, name="PromptNode", inputs=["Retriever"])

        return pricesPipeline

# pricesPipeline = PricesNode().pipeline()
# pricesDocumentStore = PricesNode().documentStore()

# output = pricesPipeline.run(query="What was the closing price of gold on October 17 2023",documents=pricesDocumentStore.get_all_documents())
# answer = output["answers"][0].answer
# print(answer)