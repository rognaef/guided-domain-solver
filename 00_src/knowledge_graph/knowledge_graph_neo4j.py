import os
from dotenv import load_dotenv
from pathlib import Path
from neo4j import GraphDatabase

class KnowledgeGraphNeo4J():
    uri : str
    auth : tuple[str, str]

    def __init__(self) -> None:
        load_dotenv(dotenv_path=Path(Path(os.path.dirname(__file__)).parent, ".env"))
        # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
        self.uri = os.getenv("NEO4J_URI")
        self.auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))


    def check_connectivity(self) -> None:
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            driver.verify_connectivity()

