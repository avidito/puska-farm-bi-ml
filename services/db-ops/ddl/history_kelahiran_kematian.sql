-- Table
CREATE TABLE history_kelahiran_kematian (
	id BIGSERIAL,
	tgl_pencatatan DATE,
	jml_lahir_pedaging_jantan INT4,
	jml_lahir_pedaging_betina INT4,
	jml_lahir_perah_jantan INT4,
	jml_lahir_perah_betina INT4,
	jml_mati_pedaging_jantan INT4,
	jml_mati_pedaging_betina INT4,
	jml_mati_perah_jantan INT4,
	jml_mati_perah_betina INT4,
	jml_mati_pedaging_anakan_jantan INT4,
	jml_mati_pedaging_anakan_betina INT4,
	jml_mati_perah_anakan_jantan INT4,
	jml_mati_perah_anakan_betina INT4,
	created_at TIMESTAMP(0),
	updated_at TIMESTAMP(0),
	deleted_at TIMESTAMP(0),
	created_by INT8,
	updated_by INT8,
	deleted_by INT8,
	id_peternak INT8,
	CONSTRAINT history_kelahiran_kematian_pkey PRIMARY KEY (id)
);

-- Inject
COPY history_kelahiran_kematian
FROM '/seed/history_kelahiran_kematian.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
