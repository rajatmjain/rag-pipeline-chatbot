from sql_node import SQLNode
from haystack.pipelines import Pipeline

class SQL:

    def __init__(self) -> None:
        pass

    def pipeline(self) -> Pipeline:
        return SQLNode().pipeline()