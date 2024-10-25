# llm-computer-science-theory-qa

# Introduction

This project will consist in a chatbot that will answer some computer science questions, based on the intents provided by [Computer Science Dataset](https://www.kaggle.com/datasets/mujtabamatin/computer-science-theory-qa-dataset) and [500 Data Science Interview Questions and Answers by Vamsee Puligadda
](https://www.kobo.com/us/es/ebook/500-data-science-interview-questions-and-answers?srsltid=AfmBOoqgwhGfV3MCxYC-YhUD98bP_-yQUTSM51PPpohxc-f-sYy3Rchr). The user will be able to give feedback to the model, through the interface. The project will include: a RAG for choosing the questions more similar to the user query, a monitoring dasboard to control costs and analyze different models and metrics, evaluation pipelines for the vector database retrieval and prompting/llm response, and orchestration tool for handling the connections between modules.

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

## Local Env Setup
1. Create a data folder in the project directory
2. Get the json from the kaggle link and save it in the data folder.
3. Get the book's pdf. Create inside the data folder a books folder and save the pdf inside it.
4. Copy `.env_example`, renamed the file into `.env` and fill the fields with your values.

## Local Env Podman Setup

1. From the project folder `podman compose up -d` to run the podman 

# Steps

The steps are the generic steps of a RAG system.

## Creating the knowledge base:

1. Preprocessing:
    - Book: First, the text is extracted from the pdf and then the text is formatted in json with the question number, the question text and the answer. [add_pdf_books.ipynb](src/preprocessing/add_pdf_books.ipynb)
    - Unify both book and cs qa jsons into one. [unify_qa_files.py](src/preprocessing/unify_qa_files.py)
    - Cleaning the duplicated questions and answers. [dataset_cleaning.ipynb](src/preprocessing/dataset_cleaning.ipynb)
    - Test there is no collisions with the ids. [test_qa_id_collisions.py](src/preprocessing/test_qa_id_collisions.py)
1. Upload the info into the vector database:
    - Start the docker compose. Run in the terminal `docker compose up`.
    - Run [indexing_documents.py](src/retrieval/indexing_documents.py). This file will:
        - Create the index in the vector database if the index does not exist or ELASTICSEARCH_FORCE_RECREATE=True in the `.env`. The name that will be used is the one stablished at the `.env` at ELASTICSEARCH_INDEX_NAME or you can specify one when instancing the IndexDocuments class.
        - Index the questions and answers in the vector database. You can specify the embedding model when instancing the IndexDocuments class or it will depend on the EMBEDDING_CLIENT defined in the `.env`. The specific model name depending on the chosen client.

## Preparing the retrieval evaluation
This step considers that you already have the documents indexed.
1. Generate the ground truth data running [create_ground_truth.ipynb](src/evaluation/create_ground_truth.ipynb). I have used Azure OpenAI with gpt-4o to create the ground truth, but you can use whatever you like.
2. 