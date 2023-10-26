import os
import pandas as pd
import sqlite3
from haystack.nodes import PromptNode,PromptTemplate,AnswerParser, MultiModalRetriever, BM25Retriever, TfidfRetriever
from haystack.document_stores import SQLDocumentStore, InMemoryDocumentStore
from haystack.pipelines import Pipeline
from haystack import Document
from sympy import true


class PricesNode:

    def __init__(self) -> None:
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME")

    # def documentStore(self) -> SQLDocumentStore:
    #     documentStore = SQLDocumentStore(url="sqlite:///data/database.db")
    #     conn = sqlite3.connect("data/database.db")
    #     df = pd.read_sql_query("SELECT * from gold_prices", conn)

    #     docs = []

    #     for index, row in df.iterrows():
    #         # Create a string in key-value format
    #         row_string = f"Date: {row['Date']} Open: {row['Open']} High: {row['High']} Low: {row['Low']} Close: {row['Close']} Volume: {row['Volume']}"

    #         # Create a Document for each row
    #         doc = Document(
    #             content=row_string,
    #             content_type="text",
    #             meta={},
    #         )

    #         docs.append(doc)

    #     # Write the Documents to the DocumentStore
    #     documentStore.write_documents(documents=docs)

    #     return documentStore

    # def retriever(self) -> SQLRetriever:
    #     retriever = SQLRetriever(document_store=self.documentStore())
    #     return retriever

    # def documentStore(self) -> InMemoryDocumentStore:
    #     documentStore = InMemoryDocumentStore(use_bm25=True)
    #     conn = sqlite3.connect("data/database.db")
    #     df = pd.read_sql_query("SELECT * from gold_prices", conn)

    #     docs = []

    #     for index, row in df.iterrows():
    #         # Create a string in key-value format
    #         row_string = f"On {row['Date']} the opening price was ${row['Open']}, the high was ${row['High']}, the low was ${row['Low']}, the closing was ${row['Close']} and the volume was {row['Volume']}"

    #         # Create a Document for each row
    #         doc = Document(
    #             content=row_string,
    #             content_type="text",
    #             meta={},
    #         )

    #         docs.append(doc)

    #     # Write the Documents to the DocumentStore
    #     documentStore.write_documents(documents=docs)

    #     return documentStore
    
    def documentStore(self) -> InMemoryDocumentStore:
        documentStore = InMemoryDocumentStore()
        conn = sqlite3.connect("data/database.db")
        df = pd.read_sql_query("SELECT * from gold_prices", conn)

        rows_summary = []

        for index, row in df.iterrows():
            # Create a sentence summarizing each row
            row_summary = f"On {row['Date']}, the opening price was ${row['Open']}, the high was ${row['High']}, the low was ${row['Low']}, the closing was ${row['Close']}, and the volume was {row['Volume']}."
            rows_summary.append(row_summary)

        # Create a single long document with all the row summaries
        long_document = Document(
            content=" ".join(rows_summary),
            content_type="text",
            meta={},
        )

        # Write the long document to the DocumentStore
        documentStore.write_documents(documents=[long_document])
        return documentStore


    def retriever(self) -> TfidfRetriever:
        documentStore = self.documentStore()
        retriever = TfidfRetriever(document_store=documentStore,top_k=3,auto_fit=true)
        return retriever
    
    def pipeline(self) -> Pipeline:
        # Prompt Template
        promptTemplate = PromptTemplate(prompt = 
                               """" You are a pipeline for getting data of prices of gold from a document. The document has sentences having information example: On 2023-10-24, the opening price was $1970.300048828125, the high was $1975.0, the low was $1970.300048828125, the closing was $1975.0, and the volume was 10.
                                Strictly answer the following query briefly based on the provided data from the document and nothing else.
                                If the context does not include an answer, reply with 'The data does not contain information related to the question'.\n
                                Query: {query}\n
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

pricesPipeline = PricesNode().pipeline()

output = pricesPipeline.run(query="What was the opening price of gold on October 26, 2023")
answer = output["answers"][0].answer
print(answer)