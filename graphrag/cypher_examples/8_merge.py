# Usa MERGE para garantir a existência de um nó no grafo
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MERGE (u:Usuario {nome:'João'})

RETURN u
"""

grafo.query(query)

print("MERGE executado com sucesso!")
