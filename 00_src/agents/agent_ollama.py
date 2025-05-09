from langchain_ollama import ChatOllama
from collections.abc import Sequence

class AgentOllama():
    llm: ChatOllama
    chain: list

    def __init__(self, model:str):
        self.llm = ChatOllama(model=model, temperature=0)
        self.chain = []

    def prompt(self, messages: Sequence) -> str:
        self.chain.extend(messages)
        result = self.llm.invoke(self.chain).content
        self.chain.append(("ai", result))
        return result
    
    def reset(self):
        self.chain.clear()