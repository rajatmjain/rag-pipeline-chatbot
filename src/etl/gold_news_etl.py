# + tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None


# +
import os
import yfinance as yf
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import LinkContentFetcher,DensePassageRetriever

# +
def newsRetriever():
    gold = yf.Ticker("GC=F")
    news = gold.news
    return news

# +
def linkRetriever(news):
    links = []

    for new in news:
        links.append(new["link"])
        return links

# +
def linkContentFetcher(links):
    lcf = LinkContentFetcher()
    docs = []

    for link in links:
        docs.append(lcf.fetch(link)[0])
        
    return docs

# +
def faissDocumentStore(docs):
    documentStore : FAISSDocumentStore

    if os.path.exists("data/faiss/faiss_index"):
        documentStore = FAISSDocumentStore.load(index_path="data/faiss/faiss_index") 
    
    else:
        documentStore = FAISSDocumentStore(sql_url="sqlite:///data/faiss/faiss_document_store.db",faiss_index_factory_str="Flat", return_embedding=True)
    
    documentStore.write_documents(docs)

    retriever = DensePassageRetriever(
                document_store=documentStore,
                query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                use_gpu=True,
                embed_title=True,
    )

    documentStore.update_embeddings(retriever)
    documentStore.save("data/faiss/faiss_index")

    return documentStore

# +
def main():
    goldNews = newsRetriever()
    newsLinks = linkRetriever(goldNews)
    content = linkContentFetcher(newsLinks)
    faissDocumentStore(content)


# -

if __name__ == "__main__":
    main()
