-- Table
CREATE TABLE public.history_populasi (
  id BIGSERIAL,
  tgl_pencatatan DATE,
  jml_pedaging_jantan INT4,
  jml_pedaging_betina INT4,
  jml_pedaging_anakan_jantan INT4,
  jml_pedaging_anakan_betina INT4,
  jml_perah_jantan INT4,
  jml_perah_betina INT4,
  jml_perah_anakan_jantan INT4,
  jml_perah_anakan_betina INT4,
  created_dt TIMESTAMP(0),
  modified_dt TIMESTAMP(0),
  deleted_at TIMESTAMP(0),
  created_by INT8,
  updated_by INT8,
  deleted_by INT8,
  id_peternak INT8,
  CONSTRAINT history_populasi_pkey PRIMARY KEY (id)
);

-- Inject
COPY history_populasi
FROM '/seed/history_populasi.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
