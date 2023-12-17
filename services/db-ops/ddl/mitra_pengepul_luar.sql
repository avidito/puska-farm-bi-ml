-- Table
CREATE TABLE mitra_pengepul_luar (
	id BIGSERIAL,
	nama_pengepul VARCHAR(255),
	jenkel VARCHAR(255),
	pendidikan VARCHAR(255),
	tgl_lahir DATE,
	jenis_pengepul VARCHAR(255),
	provinsi_id VARCHAR(64),
	kota_id VARCHAR(64),
	kecamatan_id VARCHAR(64),
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	id_unit_ternak INT8,
	CONSTRAINT mitra_pengepul_luar_jenis_pengepul_check CHECK (((jenis_pengepul)::text = ANY (ARRAY[('Ternak Potong'::character varying)::text, ('Susu'::character varying)::text]))),
	CONSTRAINT mitra_pengepul_luar_jenkel_check CHECK (((jenkel)::text = ANY (ARRAY[('Pria'::character varying)::text, ('Wanita'::character varying)::text]))),
	CONSTRAINT mitra_pengepul_luar_pendidikan_check CHECK (((pendidikan)::text = ANY (ARRAY[('Sekolah Dasar'::character varying)::text, ('Sekolah Menengah Pertama'::character varying)::text, ('Sekolah Menengah Atas'::character varying)::text, ('Strata 1 / Sarjana'::character varying)::text, ('Strata 2 / Magister'::character varying)::text, ('Strata 3'::character varying)::text]))),
	CONSTRAINT mitra_pengepul_luar_pkey PRIMARY KEY (id)
);

-- Inject
COPY mitra_pengepul_luar
FROM '/seed/mitra_pengepul_luar.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
