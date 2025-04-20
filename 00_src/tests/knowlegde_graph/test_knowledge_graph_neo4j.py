from knowledge_graph.knowledge_graph_neo4j import KnowledgeGraphNeo4J

# set up
testee = KnowledgeGraphNeo4J()

def test_check_connectivity():
    testee.check_connectivity()