# BFS - Breadth First Search
#
# Pergunta: quem esta perto de Joao na rede social?
# O BFS explora a rede em camadas: distancia 0, depois 1, depois 2...
from collections import deque

from grafo_utils import (
    carregar_amizades,
    conectar,
    grafo_nao_direcionado,
    imprimir_titulo,
)


def bfs(adjacencias, origem, profundidade_maxima=2):
    fila = deque([(origem, 0)])
    visitados = {origem}
    resultado = []

    while fila:
        pessoa, profundidade = fila.popleft()
        resultado.append((pessoa, profundidade))

        if profundidade == profundidade_maxima:
            continue

        for vizinho in adjacencias.get(pessoa, []):
            if vizinho in visitados:
                continue

            visitados.add(vizinho)
            fila.append((vizinho, profundidade + 1))

    return resultado


grafo = conectar()
arestas = carregar_amizades(grafo)
adjacencias = grafo_nao_direcionado(arestas)

imprimir_titulo("BFS - busca em largura")

for pessoa, profundidade in bfs(adjacencias, "João", profundidade_maxima=2):
    print(f"{pessoa}: distância {profundidade}")
