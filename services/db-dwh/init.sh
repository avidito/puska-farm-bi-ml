# Table
ls /ddl | while read query
do
  psql -U $POSTGRES_USER -d $POSTGRES_DB -f /ddl/$query -q
done