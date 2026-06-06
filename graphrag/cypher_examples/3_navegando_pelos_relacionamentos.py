# Navega pelos relacionamentos do grafo e mostra os amigos de João
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (joao:Usuario {nome:'João'})-[:AMIGO_DE]->(amigo)

RETURN amigo.nome
"""

resultado = grafo.ro_query(query).result_set

print("Amigos do João:")

for linha in resultado:
    print(linha[0])
