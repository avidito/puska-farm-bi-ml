-- Table
CREATE TABLE unit_ternak (
	id BIGSERIAL,
	nama_unit VARCHAR(255),
	alamat TEXT,
	provinsi_id VARCHAR(64),
	kota_id VARCHAR(64),
	kecamatan_id VARCHAR(64),
	kelurahan_id VARCHAR(64),
	latitude NUMERIC(10, 8),
	longitude NUMERIC(11, 8),
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	CONSTRAINT unit_ternak_pkey PRIMARY KEY (id)
);

-- Inject
COPY unit_ternak
FROM '/seed/unit_ternak.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
