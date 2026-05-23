# Usa OPTIONAL MATCH para retornar dados relacionais opcionais
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (u:Usuario)

OPTIONAL MATCH (u)-[:CRIOU]->(post)

RETURN u.nome, post.conteudo
"""

resultado = grafo.ro_query(query).result_set

for linha in resultado:
    print(linha)
