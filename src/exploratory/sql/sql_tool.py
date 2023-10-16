from haystack.agents import Tool
from src.exploratory.sql.sql_node import SQLNode

class SQLTool():
    def __init__(self) -> None:
        pass

    def tool():
        sqlNode = SQLNode()
        sqlDocumentStore = sqlNode.documentStore()
        sqlPipeline = sqlNode.pipeline()
        sqlTool = Tool(
            name="SQLTool",
            description="Tool to get insights from gold prices data",
            pipeline_or_node=sqlPipeline,
            output_variable="result", 
        )
        return sqlTool