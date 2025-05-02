import os
from dotenv import load_dotenv
from pathlib import Path
from neo4j import GraphDatabase

class Neo4jClient():
    uri : str
    auth : tuple[str, str]
    database : str

    def __init__(self) -> None:
        load_dotenv(dotenv_path=Path(Path(os.path.dirname(__file__)).parent, ".env"))
        # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
        self.uri = os.getenv("NEO4J_URI")
        self.auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        self.database = "neo4j"
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)
    
    def __del__(self) -> None:
        self.driver.close()

    def check_connectivity(self) -> None:
        self.driver.verify_connectivity()

    def write(self, *cyphers: str) -> None:
        with self.driver.session(database=self.database) as session:
            for cypher in cyphers:
                session.execute_write(_execute_write_tx, cypher)
                print("successful write:", " ".join(cypher.split()))

    def read(self, cypher: str, **kwargs: any) -> tuple[any, any, any]:
        records, summary, keys = self.driver.execute_query(
            cypher,
            **kwargs,
            database_=self.database)
        print("successful read:", " ".join(cypher.split()))
        return records, summary, keys

    def clear_db(self) -> None:
        with self.driver.session(database=self.database) as session:
            session.execute_write(_clear_db_tx)
            print("cleared all nodes in " + self.database)

def _execute_write_tx(tx, cypher: str) -> None:
    tx.run(cypher) 
    
def _clear_db_tx(tx) -> None:
    # delete all nodes with relationships
    tx.run("""
        MATCH (a) -[r] -> () DELETE a, r
    """) 
    # delete nodes that have no relationships
    tx.run("""
        MATCH (a) DELETE a
    """)