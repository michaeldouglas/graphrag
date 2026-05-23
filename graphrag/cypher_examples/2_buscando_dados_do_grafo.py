# Busca dados do grafo e imprime os usuários encontrados
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (u:Usuario)
RETURN u.nome
"""

resultado = grafo.ro_query(query).result_set

print("Usuários encontrados:")

for linha in resultado:
    print(linha[0])
