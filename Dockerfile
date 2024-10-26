# Dockerfile for the Streamlit service with Miniconda

# Use Miniconda3 as the base image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy environment.yaml file to the working directory
COPY environment.yaml .

# Install dependencies from environment.yaml
RUN conda env create -f environment.yaml

# Activate the environment
SHELL ["conda", "run", "-n", "cs-qa", "/bin/bash", "-c"]

# Make sure to expose the Streamlit default port
EXPOSE 8501

# Copy only the required directories and main entry script
COPY src/ ./src
COPY templates/ ./templates
COPY __main__.py .

# Set the entrypoint to run Streamlit
ENTRYPOINT ["conda", "run", "-n", "cs-qa", "streamlit", "run", "__main__.py", "--server.port=8501", "--server.address=0.0.0.0"]
