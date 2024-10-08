#!/bin/bash

CONTAINER_PREFIX="demo-store"

python3 -m venv venv
source venv/bin/activate activate
eval "$(pyenv init -)"
pip install -r requirements.txt

export FASTAPI_APP=./run.py
echo "Starting migrations..."

check_and_run_qdrant() {
    if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-qdrant)" ]; then
        echo "${CONTAINER_PREFIX}-qdrant is already running."
    else
        if [ "$(docker ps -aq -f name=${CONTAINER_PREFIX}-qdrant)" ]; then
            echo "${CONTAINER_PREFIX}-qdrant container exists but not running. Starting..."
            docker start ${CONTAINER_PREFIX}-qdrant
            echo "Qdrant container started."
        else
            echo "${CONTAINER_PREFIX}-qdrant container does not exist. Creating and starting..."
            docker run -d --name ${CONTAINER_PREFIX}-qdrant \
                -p 6333:6333 \
                -v $(pwd)/storage/qdrant:/qdrant/storage \
                qdrant/qdrant:latest
            echo "Qdrant container created and started."
        fi
    fi
}

check_and_run_postgres() {
    if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-postgres)" ]; then
        echo "${CONTAINER_PREFIX}-postgres is already running."
    else
        if [ "$(docker ps -aq -f name=${CONTAINER_PREFIX}-postgres)" ]; then
            echo "${CONTAINER_PREFIX}-postgres container exists but not running. Starting..."
            docker start ${CONTAINER_PREFIX}-postgres
            echo "Postgres container started."
        else
            echo "${CONTAINER_PREFIX}-postgres container does not exist. Creating and starting..."
            docker run -d --name ${CONTAINER_PREFIX}-postgres \
                -e POSTGRES_PASSWORD=postgres \
                -p 5432:5432 \
                -v $(pwd)/storage/postgres:/var/lib/postgresql/data \
                postgres:latest
            echo "Postgres container created and started."
        fi
    fi
}

check_and_run_qdrant
check_and_run_postgres

if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-postgres)" ] && [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-qdrant)" ]; then
    echo "Both containers are running. Starting migrations..."
    # alembic upgrade head
    python3 ./run.py
else
    echo "One or both containers failed to start. Exiting..."
    exit 1
fi
