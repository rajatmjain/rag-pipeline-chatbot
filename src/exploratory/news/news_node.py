import os
import yfinance as yf
from haystack.nodes import LinkContentFetcher, BM25Retriever, AnswerParser, DensePassageRetriever, EmbeddingRetriever, PromptNode
from haystack.document_stores import InMemoryDocumentStore, FAISSDocumentStore
from haystack.nodes.prompt import PromptTemplate
from haystack import Pipeline
from haystack.utils import print_answers

class NewsNode():
    