CREATE TABLE wilayah (
	id BIGSERIAL,
	kode VARCHAR(13),
	nama VARCHAR(100),
	CONSTRAINT wilayah_pkey PRIMARY KEY (id)
);

COPY wilayah
FROM '/seed/wilayah.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
