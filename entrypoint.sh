#!/bin/bash

# Run uvicorn using poetry
poetry run uvicorn src.main:app --host "0.0.0.0" --port 8000