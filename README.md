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

<br/>

<div align="center">
    <img src="docs/images/method_overview.drawio.svg" width="98%">
</div>

<br/>

## Description


### Knowledge Graph
<div align="center">
    <img src="docs/images/KG_Environment.drawio.svg" width="60%">
</div>

## Installation

This guide walks you through setting up the environment required to run the repository. It covers setting up the project locally from its repository, along with installing and configuring a Neo4J database and an Ollama agent system.

Make sure the following are installed on your system:

- [Python 3.10](https://www.python.org/downloads/)
- [Neo4J Desktop or Neo4J Aura](https://neo4j.com/download/)
- [Ollama](https://ollama.com/)
- [Git](https://git-scm.com/)

### 1. Repository Setup

Clone the repository and install the Python dependencies in a virtual environment:

```bash
git clone <copied URL>
cd <new directory>

# Create and activate a virtual environment
python -m venv venv

# For Windows
venv\Scripts\activate.bat

# For macOS/Linux
# source venv/bin/activate

# Install repository dependencies
pip install -r requirements.txt
```

### 2. Neo4J Database

Create an empty Neo4J database instance and ensure the [APOC plugin](https://neo4j.com/docs/apoc/current/installation/#apoc) is installed and activated.

To connect the repository to your Neo4J instance, create a `.env` file inside the <a href="src/" target="_blank">`src/`</a> directory with the following content:

```
NEO4J_URI = <URI for Neo4j database>
NEO4J_USERNAME = <Username for Neo4j>
NEO4J_PASSWORD = <Password for Neo4j>
```

Replace the values with the credentials for your Neo4J instance and make sure the database is running.

### 3. Ollama Agent System

Pull the required model using Ollama:

```bash
ollama pull qwen3:8b
```

This command downloads the qwen3:8b model, which the agent system will use during runtime.
Make sure the Ollama service is running in the background.

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