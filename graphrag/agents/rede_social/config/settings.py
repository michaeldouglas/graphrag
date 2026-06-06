import os

MODEL = os.getenv("MODEL", "gpt-oss:120b-cloud")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
