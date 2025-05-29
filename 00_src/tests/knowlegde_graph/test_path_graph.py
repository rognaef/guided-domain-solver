import pytest
from environment.const import UP
from knowledge_graph.path_graph import PathGraph 
from knowledge_graph.client_neo4j import Neo4jClient

neo4j_client = Neo4jClient()

@pytest.fixture()
def client():
    # Before each
    neo4j_client.clear_db()
    yield neo4j_client
    # After each
    # Nothing


def test_init_path(client):
    testee = PathGraph(client)
    records, summary, keys = testee.client.read("""
                                MATCH (n:Path) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 1

def test_step(client):
    testee = PathGraph(client)
    testee.step(UP, 0, False)
    records, summary, keys = testee.client.read("""
                                MATCH (n:Path) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 2

def test_set_state(client):
    testee = PathGraph(client)
    testee.step(UP, 0, False)
    assert testee.set_state([UP]) == None

def test_set_state_exception(client):
    testee = PathGraph(client)
    with pytest.raises(Exception):
        testee.set_state([UP])