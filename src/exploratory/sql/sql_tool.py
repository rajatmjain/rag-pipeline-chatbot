from haystack.agents import Tool
from sql_node import SQLNode
from sql import SQL

class SQLTool():
    def __init__(self) -> None:
        pass

    def tool():
        sql = SQL()
        sqlDocumentStore = SQLNode().documentStore()
        sqlPipeline = sql.pipeline()
        sqlTool = Tool(
            name="SQLTool",
            description="Tool to get insights from gold prices data",
            pipeline_or_node=sqlPipeline,
            output_variable="result", 
        )
        return sqlTool