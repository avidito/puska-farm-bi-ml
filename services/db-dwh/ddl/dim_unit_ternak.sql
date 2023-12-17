-- Table
CREATE TABLE dim_unit_ternak (
    id SERIAL,
    id_lokasi INT8,
    nama_unit VARCHAR(100),
    alamat TEXT,
    longitude NUMERIC(12,10),
    latitude NUMERIC(12,10),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_unit_ternak_pkey PRIMARY KEY(id)
);
