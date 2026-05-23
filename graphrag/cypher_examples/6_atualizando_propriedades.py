# Atualiza propriedades de nós no grafo
from falkordb import FalkorDB

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

query = """
MATCH (joao:Usuario {nome:'João'})

SET joao.idade = 28

RETURN joao
"""

grafo.query(query)

print("Idade adicionada com sucesso!")
