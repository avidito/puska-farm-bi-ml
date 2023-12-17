-- Table
CREATE TABLE distribusi_ternak (
	id BIGSERIAL,
	tgl_distribusi DATE,
	jumlah NUMERIC(8, 2),
	satuan VARCHAR(255),
	harga_berlaku INT4,
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	id_unit_ternak INT8,
	id_jenis_produk INT8,
	id_mitra_bisnis INT8,
	CONSTRAINT distribusi_ternak_pkey PRIMARY KEY (id)
);

-- Inject
COPY distribusi_ternak
FROM '/seed/distribusi_ternak.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");