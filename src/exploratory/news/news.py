from news_node import NewsNode
from haystack.pipelines import Pipeline

class News():

    def __init__(self) -> None:
        pass

    def pipeline(self) -> Pipeline :
        return NewsNode().pipeline()

