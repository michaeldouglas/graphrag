# Remove relacionamentos existentes no grafo
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (a:Usuario)-[r:AMIGO_DE]->(b:Usuario)

DELETE r
"""

grafo.query(query)

print("Relacionamentos removidos!")
