# Cria um grafo de exemplo e executa consultas básicas no FalkorDB
from falkordb import FalkorDB

# Connect to FalkorDB (no authentication — default Docker setup)
client = FalkorDB(host="localhost", port=6379)
graph = client.select_graph('social')


create_query = """
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
"""

graph.query(create_query)
print("Graph created successfully!")


# Find all friends of Alice
query = """
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"""

result = graph.ro_query(query).result_set

print("Alice's friends:")
for record in result:
    print(record[0])


# Find posts created by Bob
query = """
MATCH (bob:User {name: 'Bob'})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
"""

result = graph.ro_query(query).result_set

print("Posts created by Bob:")
for record in result:
    print(record[0])
