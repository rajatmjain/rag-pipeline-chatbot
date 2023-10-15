from sql_query_generator import SQLQueryGenerator

query = "Give me the 10 latest data"
sqlQueryGenerator = SQLQueryGenerator()
sqlQuery = sqlQueryGenerator.generateSQL(query=query)
print(sqlQuery)