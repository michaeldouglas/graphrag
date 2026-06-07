# Shortest Path
#
# Pergunta: qual e o menor caminho entre Joao e Carlos?
# Aqui usamos Cypher para buscar o caminho na base e imprimimos a trilha.
from grafo_utils import conectar, imprimir_titulo


grafo = conectar()

query = """
MATCH (origem:Usuario {nome: 'João'}), (destino:Usuario {nome: 'Carlos'})
WITH shortestPath((origem)-[:AMIGO_DE*]->(destino)) AS caminho
RETURN [n IN nodes(caminho) | n.nome] AS pessoas,
       length(caminho) AS distancia
"""

resultado = grafo.ro_query(query).result_set

imprimir_titulo("Shortest Path - menor caminho")

if not resultado:
    print("Nenhum caminho encontrado entre João e Carlos.")
else:
    pessoas, distancia = resultado[0]
    print(" -> ".join(pessoas))
    print(f"Distância: {distancia} saltos")
