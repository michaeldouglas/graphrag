import streamlit as st

from langchain_core.messages import HumanMessage

from agents.social_agent import agent


st.set_page_config(
    page_title="Falkordb",
    page_icon="🤖",
    layout="wide"
)

st.title("Falkordb - Agente de Rede Social")

# Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []


# Renderiza histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Input do usuário
prompt = st.chat_input("Digite sua pergunta...")


if prompt:

    # Mostra mensagem do usuário
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Chama o agente
    resposta = agent.invoke({
        "messages": [
            HumanMessage(content=prompt)
        ]
    })

    conteudo = resposta["messages"][-1].content

    # Mostra resposta
    with st.chat_message("assistant"):
        st.markdown(conteudo)

    # Salva histórico
    st.session_state.messages.append({
        "role": "assistant",
        "content": conteudo
    })
