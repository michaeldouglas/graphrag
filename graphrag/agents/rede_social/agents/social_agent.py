from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from config.settings import *

from prompts.social_prompt import SYSTEM_PROMPT
from tools.social_tools import buscar_dados_sociais


llm = init_chat_model(
    model=MODEL,
    model_provider=MODEL_PROVIDER,
    base_url=BASE_URL,
    temperature=TEMPERATURE,
)

agent = create_agent(
    model=llm,
    tools=[buscar_dados_sociais],
    system_prompt=SYSTEM_PROMPT,
)
