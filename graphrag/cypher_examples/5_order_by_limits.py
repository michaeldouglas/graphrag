# Ordena resultados e aplica limite em consultas ao grafo
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (u:Usuario)

RETURN u.nome, u.id

ORDER BY u.id DESC

LIMIT 2
"""

resultado = grafo.ro_query(query).result_set

print("Usuários ordenados:")

for linha in resultado:
    print(linha)
