# CDLP - Community Detection Label Propagation
#
# Pergunta: quais comunidades surgem pela vizinhanca?
# Cada usuario comeca com seu proprio rotulo e adota o rotulo mais comum
# entre seus vizinhos ao longo das iteracoes.
from collections import Counter, defaultdict

from grafo_utils import (
    carregar_amizades,
    conectar,
    grafo_nao_direcionado,
    imprimir_titulo,
)


def cdlp(adjacencias, iteracoes=10):
    labels = {
        no: no
        for no in adjacencias
    }

    for _ in range(iteracoes):
        mudou = False

        for no in sorted(adjacencias):
            votos = Counter(
                labels[vizinho]
                for vizinho in adjacencias[no]
            )

            if not votos:
                continue

            novo_label = votos.most_common(1)[0][0]

            if labels[no] != novo_label:
                labels[no] = novo_label
                mudou = True

        if not mudou:
            break

    comunidades = defaultdict(list)

    for no, label in labels.items():
        comunidades[label].append(no)

    return {
        label: sorted(membros)
        for label, membros in comunidades.items()
    }


grafo = conectar()
arestas = carregar_amizades(grafo)
adjacencias = grafo_nao_direcionado(arestas)
comunidades = cdlp(adjacencias)

imprimir_titulo("CDLP - detecção de comunidades")

for indice, membros in enumerate(comunidades.values(), start=1):
    print(f"Comunidade {indice}: {', '.join(membros)}")
