FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yaml .

RUN conda env create -f environment.yaml

SHELL ["conda", "run", "-n", "cs-qa", "/bin/bash", "-c"]

EXPOSE 8501

COPY src/ ./src
COPY templates/ ./templates
COPY __main__.py .

ENTRYPOINT ["conda", "run", "-n", "cs-qa", "streamlit", "run", "__main__.py", "--server.port=8501", "--server.address=0.0.0.0"]
