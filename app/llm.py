import os
from langchain_ollama import ChatOllama

_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(
    model="gemma3:1b",
    base_url=_base_url,
    temperature=0
)
