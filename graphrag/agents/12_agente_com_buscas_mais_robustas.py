import os
import json

from dotenv import load_dotenv
from falkordb import FalkorDB

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

load_dotenv()

# =========================================================
# CONFIGURAÇÕES
# =========================================================

MODEL = os.getenv("MODEL", "gpt-oss")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

# =========================================================
# CONEXÃO COM FALKORDB
# =========================================================

cliente = FalkorDB(
    host="localhost",
    port=6379
)

grafo = cliente.select_graph("rede_social")

# =========================================================
# SCHEMA DO GRAFO
# =========================================================

SCHEMA = """
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
"""

# =========================================================
# TOOL: MOSTRAR SCHEMA
# =========================================================


@tool
def mostrar_schema(_: str = "") -> str:
    """
    Retorna o schema atual do grafo.
    """

    return SCHEMA

# =========================================================
# TOOL: CONSULTAR GRAFO
# =========================================================


@tool
def consultar_grafo(query: str) -> str:
    """
    Executa uma query Cypher READ ONLY no FalkorDB.
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

    try:

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

# =========================================================
# LLM
# =========================================================


llm = init_chat_model(
    model=MODEL,
    model_provider=MODEL_PROVIDER,
    base_url=BASE_URL,
    temperature=TEMPERATURE,
)

# =========================================================
# AGENTE
# =========================================================

agent = create_agent(
    model=llm,

    tools=[
        mostrar_schema,
        consultar_grafo
    ],

    system_prompt="""
Você é um especialista em grafos, Cypher e FalkorDB.

Seu trabalho é:

1. Entender perguntas em linguagem natural
2. Criar queries Cypher inteligentes
3. Consultar o grafo
4. Explicar os resultados em português

REGRAS IMPORTANTES:

- Sempre utilize a ferramenta mostrar_schema primeiro
- Depois utilize consultar_grafo
- Gere SOMENTE queries READ ONLY
- Nunca use CREATE, DELETE, MERGE, SET ou DROP
- Explique os resultados de forma amigável
- Tente explorar conexões entre usuários

Exemplos úteis:

Encontrar amigos:
MATCH (u:Usuario {nome:'João'})-[:AMIGO_DE]->(amigo)
RETURN amigo.nome

Encontrar caminhos:
MATCH p = shortestPath(
  (a:Usuario {nome:'João'})-[*]-(b:Usuario {nome:'Carlos'})
)
RETURN p

Encontrar posts:
MATCH (u:Usuario)-[:CRIOU]->(p:Post)
RETURN u.nome, p.conteudo

Usuários sem amigos:
MATCH (u:Usuario)
WHERE NOT (u)-[:AMIGO_DE]->()
RETURN u.nome
"""
)

# =========================================================
# LOOP INTERATIVO
# =========================================================

print("=" * 60)
print("AGENTE FALKORDB + GPT-OSS")
print("=" * 60)

print("\nDigite 'sair' para encerrar.")

while True:

    pergunta = input("\nPergunta> ").strip()

    if pergunta.lower() in [
        "sair",
        "exit",
        "quit"
    ]:
        break

    try:

        resposta = agent.invoke({
            "messages": [
                HumanMessage(content=pergunta)
            ]
        })

        print("\nResposta:\n")

        print(
            resposta["messages"][-1].content
        )

    except Exception as erro:

        print("\nErro ao processar pergunta:")
        print(erro)

print("\nAgente finalizado.")
