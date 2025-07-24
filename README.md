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
    <strong><a href="#description">Description</a></strong>
    <strong> | </strong>
    <strong><a href="#installation">Installation</a></strong>
    <strong> | </strong>
    <strong><a href="#examples">Examples</a></strong>
    <strong> | </strong>
    <strong><a href="#results">Results</a></strong>
</div>

<div align="center">
    <img src="docs/images/method_overview.drawio.svg" width="98%">
</div>

## Description


### Knowledge Graph
<div align="center">
    <img src="docs/images/KG_Environment.drawio.svg" width="60%">
</div>

## Installation

The Neo4J database can be specified as a .env file, which can be stored inside <a href="src/" target="_blank">src</a>, with the following contents:
```
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

```python
from mcts.mcts import Builder
from mcts.selection import selection
from mcts.expansion import expansion
from mcts.simulation import simulation
from mcts.backprop import backprop
from environment.environment import SokobanEnvImpl

solver = (Builder()
          .setSelection(selection)
          .setExpansion(expansion)
          .setSimulation(simulation)
          .setBackprop(backprop)
          .build())
env = SokobanEnvImpl(use_default_env=True)
solver.solve(env, log_path="<Path>")
```

<div align="center">
    <img src="docs/images/0000_solved_env.gif" width="50%">
</div>



## Results

<div class="collage">
  <div class="row" align="center">
    <img src="docs/images/0001_solved_env.gif" width="30%">
    <img src="docs/images/0002_solved_env.gif" width="30%">
    <img src="docs/images/0003_solved_env.gif" width="30%">
  </div>
  <div class="row" align="center">
    <img src="docs/images/0004_solved_env.gif" width="30%">
    <img src="docs/images/0005_solved_env.gif" width="30%">
    <img src="docs/images/0006_solved_env.gif" width="30%">
  </div>
</div>

<br/>