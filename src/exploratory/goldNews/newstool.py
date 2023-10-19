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
            description="Tool to get insights from gold news",
            pipeline_or_node=newsPipeline,
            output_variable="result", 
        )
        return newsTool