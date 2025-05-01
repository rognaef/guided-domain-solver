import pytest
from knowledge_graph.client_neo4j import Neo4jClient

# set up
testee = Neo4jClient()

@pytest.fixture(autouse=True)
def run_around_tests():
    # Before each
    # Do nothing
    yield
    # After each
    testee.clear_db()

def test_check_connectivity():
    testee.check_connectivity()

def test_execute_write():
    testee.execute_write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)

def test_execute_query():
    testee.execute_write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)
    records, summary, keys = testee.execute_query("""
                                MATCH (n:TestNode) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 1

def test_clear_db():
    testee.execute_write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)

    testee.clear_db()

    records, summary, keys = testee.execute_query("""
                                MATCH (n:TestNode) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 0