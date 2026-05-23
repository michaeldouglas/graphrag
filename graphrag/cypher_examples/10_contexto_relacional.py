# Prepara um grafo com contexto relacional e dados de exemplo
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

grafo.query("""
MATCH (n)
DETACH DELETE n
""")

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

query = """
MATCH (usuario:Usuario)-[:AMIGO_DE]->(amigo)-[:CRIOU]->(post)

RETURN
  usuario.nome,
  amigo.nome,
  post.conteudo
"""

resultado = grafo.ro_query(query).result_set

print("Contexto relacional encontrado:")

for linha in resultado:
    print(linha)
