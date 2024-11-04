#!/bin/bash

CONTAINER_PREFIX="demo-store"

python3 -m venv venv
source venv/bin/activate activate
eval "$(pyenv init -)"
pip install -r requirements.txt

export FASTAPI_APP=./run.py
echo "Starting migrations..."

check_and_run_qdrant() {
    if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-qdrant-container)" ]; then
        echo "${CONTAINER_PREFIX}-qdrant-container is already running."
    else
        if [ "$(docker ps -aq -f name=${CONTAINER_PREFIX}-qdrant-container)" ]; then
            echo "${CONTAINER_PREFIX}-qdrant-container container exists but not running. Starting..."
            docker start ${CONTAINER_PREFIX}-qdrant-container
            echo "Qdrant container started."
        else
            echo "${CONTAINER_PREFIX}-qdrant-container container does not exist. Creating and starting..."
            docker run -d --name ${CONTAINER_PREFIX}-qdrant-container \
                -p 6333:6333 \
                -v $(pwd)/storage/qdrant:/qdrant/storage \
                qdrant/qdrant:latest
            echo "Qdrant container created and started."
        fi
    fi
}

check_and_run_postgres() {
    
    if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-postgres-container)" ]; then
        echo "${CONTAINER_PREFIX}-postgres-container is already running."
    else
        if [ "$(docker ps -aq -f name=${CONTAINER_PREFIX}-postgres-container)" ]; then
            echo "${CONTAINER_PREFIX}-postgres-container container exists but not running. Starting..."
            docker start ${CONTAINER_PREFIX}-postgres-container
            echo "Postgres container started."
        else
            echo "${CONTAINER_PREFIX}-postgres-container container does not exist. Creating and starting..."
            docker run -d --name ${CONTAINER_PREFIX}-postgres-container \
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

if [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-postgres-container)" ] && [ "$(docker ps -q -f name=${CONTAINER_PREFIX}-qdrant)" ]; then
    echo "Both containers are running. Starting migrations..."
    # alembic upgrade head
    python3 ./run.py
else
    echo "One or both containers failed to start. Exiting..."
    exit 1
fi

# login to postgres as super user
# docker exec -it demo-store-postgres-container psql -U postgres

# CREATE USER "postgres-user" WITH PASSWORD 'password';
# CREATE DATABASE search_app_psql_db OWNER "postgres-user";
# GRANT ALL PRIVILEGES ON DATABASE search_app_psql_db TO "postgres-user";
# PGPASSWORD=QqqgJrsEeBiPIYbxGRSUJXVGqYvOgWRM psql -h dpg-cs3mtu0gph6c73c4im3g-a.oregon-postgres.render.com -U demo_stor_dev_db_user demo_stor_dev_db


# Usage:
# ./migrations/migrate_psql_dev.sh create  # To create new migration
# ./migrations/migrate_psql_dev.sh upgrade  # To apply migrations
