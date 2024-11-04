export FASTAPI_APP=./run.py
echo $FASTAPI_APP

new_version=$(date +%y/%m/%d-%H:%M:%S)
echo new version: $new_version
echo $new_version > migrations/VERSION_PSQL_DEV

# trick if migration does not work. 
# make aux column in a table. once migration script is created,
# add your own migration code, then run upgrade.

# list enum tables and values
# SELECT e.enumtypid::regtype AS enum_type, e.enumlabel AS enum_value
# FROM pg_enum e
# ORDER BY e.enumtypid;

# initialize alembic migrations
# alembic init migrations/psql_dev

# If already initialized, run Alembic migration commands
if [ "$1" = "create" ]; then
  # create migration
  alembic revision --autogenerate -m "$new_version"
  # apply migration 
elif [ "$1" = "upgrade" ]; then
  alembic upgrade head
else
  echo "Usage: $0 {create|upgrade}"
fi

# Usage:
# ./migrate_psql_dev.sh create  # To create new migration
# ./migrate_psql_dev.sh upgrade  # To apply migrations
