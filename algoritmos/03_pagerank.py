# PageRank
#
# Pergunta: quem parece mais influente na rede?
# Implementacao simples em Python usando as arestas AMIGO_DE carregadas do FalkorDB.
from grafo_utils import (
    carregar_amizades,
    carregar_usuarios,
    conectar,
    grafo_direcionado,
    imprimir_titulo,
)


def pagerank(nos, adjacencias, iteracoes=20, damping=0.85):
    total = len(nos)

    if total == 0:
        return {}

    scores = {no: 1 / total for no in nos}

    for _ in range(iteracoes):
        novos_scores = {
            no: (1 - damping) / total
            for no in nos
        }

        for origem in nos:
            destinos = adjacencias.get(origem, [])

            if not destinos:
                distribuicao = scores[origem] / total
                for no in nos:
                    novos_scores[no] += damping * distribuicao
                continue

            distribuicao = scores[origem] / len(destinos)
            for destino in destinos:
                novos_scores[destino] += damping * distribuicao

        scores = novos_scores

    return scores


grafo = conectar()
usuarios = carregar_usuarios(grafo)
arestas = carregar_amizades(grafo)
adjacencias = grafo_direcionado(arestas)
scores = pagerank(usuarios, adjacencias)

imprimir_titulo("PageRank - ranking de relevância")

for pessoa, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{pessoa}: {score:.4f}")
