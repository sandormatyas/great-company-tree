# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY scripts/ /app/scripts/
COPY src/ /app/src/
COPY pyproject.toml entrypoint.sh /app/

# Grant run permission to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Install the dependencies
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-interaction --no-dev

# Expose the port that the app will run on
EXPOSE 8000
