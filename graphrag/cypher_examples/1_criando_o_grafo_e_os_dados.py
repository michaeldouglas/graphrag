# Cria o grafo e insere dados de exemplo no FalkorDB
from falkordb import FalkorDB

# conexão
cliente = FalkorDB(host="localhost", port=6379)

# seleciona/cria o grafo
grafo = cliente.select_graph("rede_social")

# limpa o grafo
grafo.query("""
MATCH (n)
DETACH DELETE n
""")

# cria os nós e relacionamentos
query = """
CREATE
  (joao:Usuario {
    id: 1,
    nome: 'João'
  }),

  (maria:Usuario {
    id: 2,
    nome: 'Maria'
  }),

  (carlos:Usuario {
    id: 3,
    nome: 'Carlos'
  }),

  (post1:Post {
    id: 101,
    conteudo: 'Olá mundo'
  }),

  (post2:Post {
    id: 102,
    conteudo: 'Grafos são incríveis'
  }),

  (joao)-[:AMIGO_DE]->(maria),
  (maria)-[:AMIGO_DE]->(carlos),

  (joao)-[:CRIOU]->(post1),
  (maria)-[:CRIOU]->(post2)
"""

grafo.query(query)

print("Grafo criado com sucesso!")
