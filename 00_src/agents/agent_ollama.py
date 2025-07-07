import os
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from collections.abc import Sequence
import logging
from logging import Logger

class AgentOllama():
    llm: ChatOllama
    prompt: ChatPromptTemplate
    chain: Runnable
    logger: Logger

    def __init__(self, model:str, message_template:Sequence, extract_reasoning= False):
        self.llm = ChatOllama(model=model, temperature=0, extract_reasoning=extract_reasoning).invoke
        self.prompt = ChatPromptTemplate.from_messages(message_template)
        self.chain = self.prompt | self.llm
        self.logger = logging.getLogger("AgentOllama_{id}".format(id = id(self)))
        self.logger.setLevel(logging.INFO)

    def invoke(self, message: Sequence) -> str:
        self.logger.info(self.prompt.invoke(message))
        answer = self.chain.invoke(message)
        self.logger.info([answer])
        return answer.content
    
    def write_log(self, log_path:str, clear_log_path=False):
        if clear_log_path and os.path.exists(log_path):
            os.remove(log_path)
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        fileHandler = logging.FileHandler(log_path, encoding='utf-8')
        fileHandler.setFormatter(logFormatter)
        self.logger.handlers.clear()
        self.logger.addHandler(fileHandler)