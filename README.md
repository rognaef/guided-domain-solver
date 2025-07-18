<div align="center">
    <h1 align=center>Code Generation with Knowledge Graph</h1>
</div>

<div align="center">
    <em>Code Generation with Knowledge Graph project is an approach to automating software development by leveraging the power of multi-agent systems and knowledge graphs. This project aims to generate code by enabling multiple intelligent agents to collaboratively generate, optimize, and validate code based on a structured knowledge graph that captures domain-specific information.</em>
</div>

<br/>

<div align="center">
<a href="https://www.python.org/doc/versions/" target="_blank"><img src="https://img.shields.io/badge/Python-3.10-color=%2334D058.svg" alt="Supported Python versions"></a>
<a href="tests/coverage.txt" target="_blank"><img src="https://img.shields.io/badge/Tests-passing-color=%2334D058.svg" alt="Tests"></a>
<a href="tests/coverage.txt" target="_blank"><img src="https://img.shields.io/badge/Coverage-99%25-color=%2334D058.svg" alt="Coverage"></a>
</div>

<br/>

<div align="center">
    <strong><a href="#description" target="_blank">Description</a></strong>
    <strong> | </strong>
    <strong><a href="#installation" target="_blank">Installation</a></strong>
    <strong> | </strong>
    <strong><a href="#examples" target="_blank">Examples</a></strong>
    <strong> | </strong>
    <strong><a href="#results" target="_blank">Results</a></strong>
</div>

<br/>

<div class="collage">
  <div class="row" align="center">
    <img src="docs/images/0000_solved_env.gif" width="30%">
    <img src="docs/images/0001_solved_env.gif" width="30%">
    <img src="docs/images/0002_solved_env.gif" width="30%">
  </div>
  <div class="row" align="center">
    <img src="docs/images/0003_solved_env.gif" width="30%">
    <img src="docs/images/0004_solved_env.gif" width="30%">
    <img src="docs/images/0005_solved_env.gif" width="30%">
  </div>
</div>

<br/>

## Description

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

The Neo4J database must have installed the plugin APOC. (see <https://neo4j.com/docs/apoc/current/installation/#apoc>)

Install requirements for python enviroment:

```console
>pip install -r requirements.txt
```

## Examples


## Results