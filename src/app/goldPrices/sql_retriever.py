from typing import List, Optional, Dict
from haystack.schema import Document
from haystack.document_stores.sql import SQLDocumentStore
from haystack.nodes import BaseRetriever

class SQLRetriever(BaseRetriever):
    def __init__(self, document_store: SQLDocumentStore):
        super().__init__()
        self.document_store = document_store

    def retrieve(
        self,
        query: str,
        filters: Optional[Dict] = None,
        top_k: Optional[int] = None,
        index: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        scale_score: Optional[bool] = None,
        document_store: Optional[SQLDocumentStore] = None,
    ) -> List[Document]:
        # Use the SQLDocumentStore to retrieve all documents
        documents = self.document_store.get_all_documents(index=index, filters=filters, headers=headers)
        print(documents)
        return documents

    def retrieve_batch(
        self,
        queries: List[str],
        filters: Optional[Dict] = None,
        top_k: Optional[int] = None,
        index: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        batch_size: Optional[int] = None,
        scale_score: Optional[bool] = None,
        document_store: Optional[SQLDocumentStore] = None,
    ) -> List[List[Document]]:
        # Use the SQLDocumentStore to retrieve all documents in batch (if needed)
        documents = self.document_store.get_all_documents(index=index, filters=filters, headers=headers)
        # You can split the documents into batches based on your batch_size if required
        return [documents]

