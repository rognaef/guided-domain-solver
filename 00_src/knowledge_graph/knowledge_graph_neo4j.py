import os
from dotenv import load_dotenv
from pathlib import Path
from neo4j import GraphDatabase

class KnowledgeGraphNeo4J():
    uri : str
    auth : tuple[str, str]
    database : str

    def __init__(self) -> None:
        load_dotenv(dotenv_path=Path(Path(os.path.dirname(__file__)).parent, ".env"))
        # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
        self.uri = os.getenv("NEO4J_URI")
        self.auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        self.database = "neo4j"

    def check_connectivity(self) -> None:
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            driver.verify_connectivity()

    def execute_write(self, cypher):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            with driver.session(database=self.database) as session:
                session.execute_write(_execute_write_tx, cypher)
                print("successful")

    def execute_query(self, query: str, **kwargs: any):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            records, summary, keys = driver.execute_query(
            query,
            **kwargs,
            database_=self.database,
            )
        return records, summary, keys

    def clear_db(self):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            with driver.session(database=self.database) as session:
                session.execute_write(_clear_db_tx)
                print("cleared all nodes in " + self.database)

def _execute_write_tx(tx, cypher):
    tx.run(cypher) 
    
def _clear_db_tx(tx):
    # delete all nodes with relationships
    tx.run("""
        MATCH (a) -[r] -> () DELETE a, r
    """) 
    # delete nodes that have no relationships
    tx.run("""
        MATCH (a) DELETE a
    """)