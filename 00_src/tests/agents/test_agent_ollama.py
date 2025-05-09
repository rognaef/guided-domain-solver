import pytest
from agents.agent_ollama import AgentOllama

# set up
testee = AgentOllama("qwen2.5-coder:7b")

@pytest.fixture(autouse=True)
def run_around_tests():
    # Before each
    # Do nothing
    yield
    # After each
    testee.reset()

def test_prompt():
    testee.prompt([("human", "hello")])
    assert len(testee.chain) == 2

def test_clear():
    testee.prompt([("human", "hello")])
    assert len(testee.chain) == 2
    testee.reset()
    assert len(testee.chain) == 0

