# agente LangChain usando Ollama/gpt-oss para consultar o grafo social

import os
from typing import List

from dotenv import load_dotenv
from falkordb import FalkorDB

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

load_dotenv()

# =========================
# CONFIGURAÇÃO DO MODELO
# =========================

MODEL = os.getenv("MODEL", "gpt-oss:20b-cloud")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

# =========================
# CONEXÃO COM FALKORDB
# =========================

cliente = FalkorDB(host="localhost", port=6379)
grafo = cliente.select_graph("rede_social")

# =========================
# HELPERS
# =========================


def safe_value(text: str) -> str:
    return text.replace("'", "\\'").strip()


def format_rows(rows: List[tuple]) -> str:
    return "\n".join(
        str(item[0]) if len(item) == 1
        else ", ".join(str(x) for x in item)
        for item in rows
    )

# =========================
# TOOLS
# =========================


@tool
def buscar_amigos(nome: str) -> str:
    """
    Retorna os amigos diretos de um usuário.
    """

    nome = safe_value(nome)

    query = f"""
    MATCH (u:Usuario {{nome: '{nome}'}})-[:AMIGO_DE]->(amigo)
    RETURN amigo.nome
    """

    resultado = grafo.ro_query(query).result_set

    if not resultado:
        return f"Nenhum amigo encontrado para {nome}."

    return f"Amigos de {nome}:\n" + format_rows(resultado)


@tool
def buscar_postagens(nome: str) -> str:
    """
    Retorna as postagens criadas por um usuário.
    """

    nome = safe_value(nome)

    query = f"""
    MATCH (u:Usuario {{nome: '{nome}'}})-[:CRIOU]->(post:Post)
    RETURN post.id, post.conteudo
    """

    resultado = grafo.ro_query(query).result_set

    if not resultado:
        return f"Nenhuma postagem encontrada para {nome}."

    return f"Postagens de {nome}:\n" + format_rows(resultado)


@tool
def contar_amigos(nome: str) -> str:
    """
    Conta quantos amigos diretos um usuário possui.
    """

    nome = safe_value(nome)

    query = f"""
    MATCH (u:Usuario {{nome: '{nome}'}})-[:AMIGO_DE]->(amigo)
    RETURN COUNT(amigo)
    """

    resultado = grafo.ro_query(query).result_set

    if not resultado or not resultado[0]:
        return f"Não foi possível contar amigos de {nome}."

    return f"{nome} tem {resultado[0][0]} amigo(s) direto(s)."


@tool
def listar_usuarios(_: str = "") -> str:
    """
    Lista todos os usuários cadastrados no grafo.
    """

    query = """
    MATCH (u:Usuario)
    RETURN u.nome
    ORDER BY u.nome
    """

    resultado = grafo.ro_query(query).result_set

    if not resultado:
        return "Nenhum usuário encontrado no grafo."

    return "Usuários no grafo:\n" + format_rows(resultado)

# =========================
# LLM
# =========================


llm = init_chat_model(
    model=MODEL,
    model_provider=MODEL_PROVIDER,
    base_url=BASE_URL,
    temperature=TEMPERATURE,
)

# =========================
# AGENTE
# =========================

agent = create_agent(
    llm,
    tools=[
        buscar_amigos,
        buscar_postagens,
        contar_amigos,
        listar_usuarios,
    ],
    system_prompt=(
        "Você é um assistente especialista em consultas "
        "de um grafo social usando FalkorDB. "
        "Utilize as ferramentas disponíveis para responder "
        "perguntas sobre usuários, amizades e postagens."
    )
)

# =========================
# LOOP INTERATIVO
# =========================

print("Exemplo: Quando amigos o joão tem?")
print("Digite 'sair' para encerrar.")

while True:

    pergunta = input("\nPergunta> ").strip()

    if pergunta.lower() in {"sair", "exit", "quit"}:
        break

    try:

        result = agent.invoke({
            "messages": [
                HumanMessage(content=pergunta)
            ]
        })

        resposta = result["messages"][-1].content

        print("\nResposta:\n")
        print(resposta)

    except Exception as error:
        print("\nErro ao processar pergunta:")
        print(error)

print("\nAgente finalizado.")
