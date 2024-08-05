# llm-computer-science-theory-qa

# Introduction

This project will consist in a chatbot that will answer some computer science questions, based on the intents provided by [Computer Science Dataset](https://www.kaggle.com/datasets/mujtabamatin/computer-science-theory-qa-dataset). The user will be able to give feedback to the model, through the interface. The project will include: a RAG for choosing the questions more similar to the user query, a monitoring dasboard to control costs and analyze different models and metrics, evaluation pipelines for the vector database retrieval and prompting/llm response, and orchestration tool for handling the connections between modules.

# Technologies:
- **Azure OpenAI**: main llm and embedding
- **Ollama**: secondary llms
- **SentenceTransformers**: secondary embedding models
- **ElasticSearch**: VectorDatabase
- **Grafana and PostGres DB**: Monitoring
- **Mage**: orchestration
- **Streamlit**: app
- **Python**: programming language
- **Docker and docker-compose**: containers and orchestration
- **Conda**: package management
- **Git and Github**: version control

# Setup

## Anaconda Commands

In the terminal run:

```
conda env create --name <project_name> --file=environment.yml
```
This will create the environment with the dependencies


For activating the conda environment the following times, run:
```
conda activate <project_name>
```