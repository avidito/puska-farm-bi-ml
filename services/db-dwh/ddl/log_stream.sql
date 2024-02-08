CREATE TABLE log_stream (
    table_name VARCHAR(100),
    mode VARCHAR(100),
    payload VARCHAR(255),
    start_tm TIMESTAMP,
    end_tm TIMESTAMP,
    duration INTEGER
);