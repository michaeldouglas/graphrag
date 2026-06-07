from collections import defaultdict
from falkordb import FalkorDB


def conectar():
    cliente = FalkorDB(host="localhost", port=6379)
    return cliente.select_graph("rede_social")


def carregar_usuarios(grafo):
    resultado = grafo.ro_query("""
    MATCH (u:Usuario)
    RETURN u.nome
    ORDER BY u.nome
    """).result_set

    return [linha[0] for linha in resultado]


def carregar_amizades(grafo):
    resultado = grafo.ro_query("""
    MATCH (a:Usuario)-[:AMIGO_DE]->(b:Usuario)
    RETURN a.nome, b.nome
    ORDER BY a.nome, b.nome
    """).result_set

    return [(linha[0], linha[1]) for linha in resultado]


def grafo_direcionado(arestas):
    adjacencias = defaultdict(list)

    for origem, destino in arestas:
        adjacencias[origem].append(destino)
        adjacencias.setdefault(destino, [])

    return dict(adjacencias)


def grafo_nao_direcionado(arestas):
    adjacencias = defaultdict(set)

    for origem, destino in arestas:
        adjacencias[origem].add(destino)
        adjacencias[destino].add(origem)

    return {
        no: sorted(vizinhos)
        for no, vizinhos in adjacencias.items()
    }


def imprimir_titulo(texto):
    print("\n" + "=" * len(texto))
    print(texto)
    print("=" * len(texto))


def imprimir_linhas(cabecalho, linhas):
    print(cabecalho)

    for linha in linhas:
        print(f"- {linha}")
