# Prepara uma rede social um pouco maior para os exemplos de algoritmos.
#
# Este script nao apaga a base existente. Ele usa MERGE para acrescentar
# usuarios e relacionamentos que deixam BFS, PageRank, Betweenness, WCC e CDLP
# mais interessantes de observar.
from falkordb import FalkorDB


cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MERGE (joao:Usuario {nome: 'João'})
  ON CREATE SET joao.id = 1
MERGE (maria:Usuario {nome: 'Maria'})
  ON CREATE SET maria.id = 2
MERGE (carlos:Usuario {nome: 'Carlos'})
  ON CREATE SET carlos.id = 3
MERGE (ana:Usuario {nome: 'Ana'})
  ON CREATE SET ana.id = 4
MERGE (pedro:Usuario {nome: 'Pedro'})
  ON CREATE SET pedro.id = 5
MERGE (lucas:Usuario {nome: 'Lucas'})
  ON CREATE SET lucas.id = 6
MERGE (beatriz:Usuario {nome: 'Beatriz'})
  ON CREATE SET beatriz.id = 7
MERGE (rafa:Usuario {nome: 'Rafa'})
  ON CREATE SET rafa.id = 8
MERGE (sofia:Usuario {nome: 'Sofia'})
  ON CREATE SET sofia.id = 9

MERGE (post1:Post {conteudo: 'Olá mundo'})
  ON CREATE SET post1.id = 101
MERGE (post2:Post {conteudo: 'Grafos são incríveis'})
  ON CREATE SET post2.id = 102
MERGE (post3:Post {conteudo: 'GraphRAG com FalkorDB'})
  ON CREATE SET post3.id = 103

MERGE (joao)-[:AMIGO_DE]->(maria)
MERGE (maria)-[:AMIGO_DE]->(carlos)
MERGE (joao)-[:AMIGO_DE]->(ana)
MERGE (ana)-[:AMIGO_DE]->(carlos)
MERGE (pedro)-[:AMIGO_DE]->(maria)
MERGE (lucas)-[:AMIGO_DE]->(maria)
MERGE (beatriz)-[:AMIGO_DE]->(maria)
MERGE (carlos)-[:AMIGO_DE]->(rafa)

MERGE (sofia)-[:AMIGO_DE]->(pedro)

MERGE (joao)-[:CRIOU]->(post1)
MERGE (maria)-[:CRIOU]->(post2)
MERGE (carlos)-[:CRIOU]->(post3)
"""

grafo.query(query)

print("Dados de algoritmos preparados na base rede_social.")
print("Agora rode, por exemplo: python algoritmos/01_bfs.py")
