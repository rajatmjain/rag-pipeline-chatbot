from haystack.agents import Tool
from goldNews.news import News

class NewsTool():
    def __init__(self) -> None:
        pass

    def tool():
        news = News()
        newsPipeline = news.pipeline()
        newsTool = Tool(
            name="NewsTool",
            description="This tool is useful for analyzing news for the commodity gold and responds with insights from the news. This tool has access to a vector database which has embeddings of documents of news articles.",
            pipeline_or_node=newsPipeline
        )
        return newsTool