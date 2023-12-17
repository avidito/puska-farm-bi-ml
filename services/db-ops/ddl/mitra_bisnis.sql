-- Table
CREATE TABLE mitra_bisnis (
	id BIGSERIAL,
	nama_mitra VARCHAR(255),
	provinsi_id VARCHAR(64),
	kota_id VARCHAR(64),
	kecamatan_id VARCHAR(64),
	kelurahan_id VARCHAR(64),
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	id_unit_ternak INT8,
	id_kategori_mitra INT8,
	CONSTRAINT mitra_bisnis_pkey PRIMARY KEY (id)
);

-- Inject
COPY mitra_bisnis
FROM '/seed/mitra_bisnis.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
