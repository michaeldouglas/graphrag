# Filtra nós no grafo usando uma condição simples
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (u:Usuario)

WHERE u.id > 1

RETURN u.nome
"""

resultado = grafo.ro_query(query).result_set

print("Usuários com ID maior que 1:")

for linha in resultado:
    print(linha[0])
