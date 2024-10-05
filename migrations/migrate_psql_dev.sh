export FLASK_APP=./run_dev.py
echo $FLASK_APP

new_version=$(date +%y/%m/%d-%H:%M:%S)
echo $new_version
echo $new_version > migrations/VERSION_DEV

flask db migrate --directory=migrations/dev -m "dev-version-$new_version"

# flask db stamp head --directory=migrations/dev
# flask db init --directory=migrations/dev
# flask db migrate --directory=migrations/dev
# flask db upgrade --directory=migrations/dev

# trick if migration does not work. 
# make aux column in a table. once migration script is created,
# add your own migration code, then run upgrade.

# list enum tables and values
# SELECT e.enumtypid::regtype AS enum_type, e.enumlabel AS enum_value
# FROM pg_enum e
# ORDER BY e.enumtypid;