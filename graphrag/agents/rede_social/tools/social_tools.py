import json

from langchain_core.tools import tool

from database.connection import grafo


@tool("buscar_dados_sociais")
def buscar_dados_sociais(query: str) -> str:
    """
    Executa queries Cypher READ ONLY
    na rede social da Alura.

    Schema do grafo:

    Nós:

    (:Usuario {
        id,
        nome
    })

    (:Post {
        id,
        conteudo
    })

    Relacionamentos:

    (:Usuario)-[:AMIGO_DE]->(:Usuario)

    (:Usuario)-[:CRIOU]->(:Post)

    Exemplos válidos:

    Encontrar amigos:
    MATCH (:Usuario {nome:'João'})-[:AMIGO_DE]->(amigo)
    RETURN amigo.nome

    Encontrar posts:
    MATCH (:Usuario {nome:'Maria'})-[:CRIOU]->(p:Post)
    RETURN p.conteudo

    Encontrar caminhos:
    MATCH p = shortestPath(
      (:Usuario {nome:'João'})-[*]-(:Usuario {nome:'Carlos'})
    )
    RETURN p

    IMPORTANTE:
    - Use SOMENTE Usuario e Post
    - Usuario possui propriedade nome
    - NÃO existe propriedade name
    - NÃO existe User
    - NÃO existe Person
    - Gere apenas queries READ ONLY
    """

    query_upper = query.upper()

    comandos_bloqueados = [
        "CREATE",
        "DELETE",
        "DETACH",
        "SET",
        "MERGE",
        "REMOVE",
        "DROP",
        "CALL"
    ]

    for comando in comandos_bloqueados:

        if comando in query_upper:

            return (
                f"Comando bloqueado por segurança: {comando}"
            )

    print("\n=== CYPHER GERADO ===")
    print(query)

    try:
        print("INICIANDO A CONSULTA AO GRAFO...")
        resultado = grafo.ro_query(query)

        if not resultado.result_set:

            return "Nenhum resultado encontrado."

        return json.dumps(
            resultado.result_set,
            ensure_ascii=False,
            indent=2
        )

    except Exception as erro:

        return f"Erro ao executar query: {erro}"
