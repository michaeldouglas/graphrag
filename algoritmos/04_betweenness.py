# Betweenness Centrality
#
# Pergunta: quem funciona como ponte entre grupos da rede?
# Para fins didaticos, calculamos todos os menores caminhos em Python.
from collections import deque

from grafo_utils import (
    carregar_amizades,
    conectar,
    grafo_nao_direcionado,
    imprimir_titulo,
)


def menor_caminho(adjacencias, origem, destino):
    fila = deque([(origem, [origem])])
    visitados = {origem}

    while fila:
        atual, caminho = fila.popleft()

        if atual == destino:
            return caminho

        for vizinho in adjacencias.get(atual, []):
            if vizinho in visitados:
                continue

            visitados.add(vizinho)
            fila.append((vizinho, caminho + [vizinho]))

    return []


def betweenness(adjacencias):
    nos = sorted(adjacencias)
    scores = {no: 0 for no in nos}

    for indice, origem in enumerate(nos):
        for destino in nos[indice + 1:]:
            caminho = menor_caminho(adjacencias, origem, destino)

            for intermediario in caminho[1:-1]:
                scores[intermediario] += 1

    return scores


grafo = conectar()
arestas = carregar_amizades(grafo)
adjacencias = grafo_nao_direcionado(arestas)
scores = betweenness(adjacencias)

imprimir_titulo("Betweenness - pontes da rede")

for pessoa, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{pessoa}: {score}")
