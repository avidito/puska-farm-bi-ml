-- Table
CREATE TABLE produksi_susu (
	id BIGSERIAL,
	tgl_produksi DATE,
	jumlah NUMERIC(8, 2),
	satuan VARCHAR(255),
	sumber_pasokan VARCHAR(255),
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	id_unit_ternak INT8,
	id_jenis_produk INT8,
	CONSTRAINT produksi_susu_pkey PRIMARY KEY (id),
	CONSTRAINT produksi_susu_sumber_pasokan_check CHECK (((sumber_pasokan)::text = ANY (ARRAY[('Peternakan Sendiri'::character varying)::text, ('Peternakan Lain'::character varying)::text, ('Pengepul'::character varying)::text])))
);

-- Inject
COPY produksi_susu
FROM '/seed/produksi_susu.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
