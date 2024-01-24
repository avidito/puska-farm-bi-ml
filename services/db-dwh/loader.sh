
psql -U $POSTGRES_USER -d $POSTGRES_DB -c "COPY fact_populasi FROM '/seed/inject_populasi_kabupaten_kota.csv' WITH (FORMAT 'csv', DELIMITER ';', HEADER TRUE, NULL 'NULL');"
