# VM Code Generation with Knowledge Graph

Code Generation with Knowledge Graph project is an approach to automating software development by leveraging the power of multi-agent systems and knowledge graphs. This project aims to generate code by enabling multiple intelligent agents to collaboratively generate, optimize, and validate code based on a structured knowledge graph that captures domain-specific information.

## Installation
Set up your development environment to use API for agents:

| API    | Quickstart link |
| -------- | ------- |
| OpenAI  | <https://platform.openai.com/docs/libraries?desktop-os=windows&language=python>|
| Anthropic  | <https://docs.anthropic.com/en/api/getting-started>|
| AI/ML API  | <https://docs.aimlapi.com/quickstart/setting-up>|

The API key and Neo4J database can be specified in a .env file which can be stored at 00_src/.env and has the following contents:

```
OPENAI_API_KEY = <YOUR_API_KEY>
OPENAI_API_BASE_URL = <YOUR_API_URL>
NEO4J_URI = <URI for Neo4j database>
NEO4J_USERNAME = <Username for Neo4j>
NEO4J_PASSWORD = <Password for Neo4j>
```

Install requirements for python enviroment:

```console
>pip install -r requirements.txt
```