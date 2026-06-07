# WCC - Weakly Connected Components
#
# Pergunta: quais ilhas conectadas existem na rede?
# Tratamos AMIGO_DE como uma conexao sem direcao para encontrar componentes.
from collections import deque

from grafo_utils import (
    carregar_amizades,
    conectar,
    grafo_nao_direcionado,
    imprimir_titulo,
)


def componentes_conectados(adjacencias):
    visitados = set()
    componentes = []

    for origem in sorted(adjacencias):
        if origem in visitados:
            continue

        componente = []
        fila = deque([origem])
        visitados.add(origem)

        while fila:
            atual = fila.popleft()
            componente.append(atual)

            for vizinho in adjacencias.get(atual, []):
                if vizinho in visitados:
                    continue

                visitados.add(vizinho)
                fila.append(vizinho)

        componentes.append(sorted(componente))

    return componentes


grafo = conectar()
arestas = carregar_amizades(grafo)
adjacencias = grafo_nao_direcionado(arestas)
componentes = componentes_conectados(adjacencias)

imprimir_titulo("WCC - componentes conectados")

for indice, componente in enumerate(componentes, start=1):
    membros = ", ".join(componente)
    print(f"Componente {indice}: {membros}")
