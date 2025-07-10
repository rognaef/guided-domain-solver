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
    testee.write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)

def test_execute_query():
    testee.write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)
    records, summary, keys = testee.read("""
                                MATCH (n:TestNode) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 1

def test_clear_db():
    testee.write("""
    CREATE (a:TestNode { Tag : "This is a test" })
    """)

    testee.clear_db()

    records, summary, keys = testee.read("""
                                MATCH (n:TestNode) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 0

def test_write_log():
    testee.write_log("../tests/knowledge_graph/output/test_write_log.log", clear_log_path=True)
    testee.write("CREATE (a:TestNode { Tag : 'This is a test' })")
    testee.read("MATCH (n:TestNode) RETURN n LIMIT $limit", limit = 25)