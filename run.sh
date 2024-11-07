#!/bin/bash

CONTAINER_PREFIX="demo-rag"

python3 -m venv venv
source venv/bin/activate activate
eval "$(pyenv init -)"
pip install -r requirements.txt

export FASTAPI_APP=./run.py

python3 ./run.py
