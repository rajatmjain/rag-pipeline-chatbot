import os
from haystack.nodes import AnswerParser, DensePassageRetriever, PromptNode
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes.prompt import PromptTemplate
from haystack import Pipeline
from haystack.utils import print_answers

class NewsNode():

    def __init__(self) -> None:
        # Model configurations
        self.hfAPIKey = os.getenv("HF_API_KEY")
        self.hfModelName = os.getenv("HF_MODEL_NAME") 
      
    def documentStore(self) -> FAISSDocumentStore:
        return FAISSDocumentStore.load(index_path="data/faiss/faiss_index")

      
    def retriever(self,documentStore) -> DensePassageRetriever:
        retriever = DensePassageRetriever(
                        document_store=documentStore,
                        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                        use_gpu=True,
                        embed_title=True,
        )

        documentStore.update_embeddings(retriever)

        documentStore.save("data/faiss/faiss_index")

        return retriever
    
    def promptNode(self) -> PromptNode:
        promptTemplate = PromptTemplate(
        prompt="""" You are an assistant getting latest news on the commodity of gold from documents.
                                Strictly answer the following query briefly based on the provided news from the documents and nothing else.
                                If the context does not include an answer, reply with 'The data does not contain information related to the question'.\n
                                Query: {query}\n
                                Documents: {documents}\n
                                Answer: 
                                """,
                                output_parser=AnswerParser(),
                                )
        
        # Prompt Node initialization
        promptNode = PromptNode(self.hfModelName,api_key=self.hfAPIKey,default_prompt_template = promptTemplate)

        return promptNode
    
    def pipeline(self) -> Pipeline:
        # Pipeline
        pipeline = Pipeline()
        pipeline.add_node(component=self.retriever(self.documentStore()), name="retriever", inputs=["Query"])
        pipeline.add_node(component=self.promptNode(), name="promptNode", inputs=["retriever"])  

        return pipeline


# news = NewsNode()
# newsDocumentStore = news.documentStore()
# newsPipeline = news.pipeline()
# output = newsPipeline.run(query="Summarize the news for me",documents=newsDocumentStore.get_all_documents())
# answer = output["answers"][0].answer
# print(answer)   
