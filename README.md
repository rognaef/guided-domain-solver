<div align="center">
    <h1 align=center>Guided Domain Solver: Structured Exploration of Domain-Specific Tasks with Large Language Models</h1>
</div>

<div align="center">
    <em>
    This project presents a method to solve domain-specific problems by leveraging Monte Carlo Tree Search (MCTS), Knowledge Graphs and Large Language Model (LLM) agents. At the core of this approach lies a MCTS algorithm, which explores the complex solution space of a given domain in a goal-directed and sample-efficient manner. In the expansion phase of the MCTS, a domain-specific knowledge graph is incorporated to encode concepts, relationships and constraints. This structured representation enables an LLM agent to make informed decisions for the node expansion. By combining a structured search of the solution space through MCTS, a representation of domain knowledge through the knowledge graph and the generalization abilities of an LLM agent, this method can solve complex tasks in domains where both creativity and adherence to expert rules are essential. In a first step, this approach is used to solve Sokoban, a puzzle game that requires planning and creativity to place several boxes at specific targets with as few moves as possible.
    </em>
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

This example demonstrates how to solve the default Sokoban environment. 
The MCTS algorithm is modular and allows you to plug in custom strategies for each phase of the search: selection, expansion, simulation, and backpropagation.

```python
from mcts.mcts import Builder
from mcts.selection import selection
from mcts.expansion import expansion
from mcts.simulation import simulation
from mcts.backprop import backprop
from environment.environment import SokobanEnvImpl

# Build the solver with custom strategies
solver = (Builder()
          .setSelection(selection)
          .setExpansion(expansion)
          .setSimulation(simulation)
          .setBackprop(backprop)
          .build())
# Initialize the default Sokoban environment
env = SokobanEnvImpl(use_default_env=True)
# Solve the environment and save logs to the specified path
solver.solve(env, log_path="<Path>")
```

The solved environment and detailed logs (including the solution) will be saved to the specified `<Path>`. 
The algorithm solves the default Sokoban environment with the shortest trajectory of 30 moves:

<div align="center">
    <img src="docs/images/0000_solved_env.gif" width="50%">
</div>

Unseen Sokoban enviroments can be generated with the following:

```python
# Generate new Sokoban environment, which resets to starting point
env = SokobanEnvImpl(max_steps=60).as_fixated()
```

The algorithm finds the shortest possible trajectory to solve the Sokoban enviroment.
Below are some generated Sokoban environments that have been solved optimally:

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

More examples can be found in the  <a href="docs/" target="_blank">`docs/`</a> directory.

## Results
