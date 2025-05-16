import os
from agents.agent_ollama import AgentOllama

# set up
testee = AgentOllama("qwen2.5-coder:7b",
                     [("system", "You are a helpful assistant that translates {input_language} to {output_language}.",),        
                      ("human", "{input}"),])

def test_invoke():
    answer = testee.invoke({
        "input_language": "English",
        "output_language": "German",
        "input": "I love programming."})
    assert answer

def test_write_log():
    testee.write_log("./tests/agents/output/test_write_log.log", clear_log_path=True)
    testee.invoke({
        "input_language": "English",
        "output_language": "German",
        "input": "I love programming."})
