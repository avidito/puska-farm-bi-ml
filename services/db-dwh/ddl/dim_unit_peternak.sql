-- Table
CREATE TABLE dim_unit_peternak (
    id INT8,
    id_lokasi INT8,
    nama_unit VARCHAR(100),
    alamat TEXT,
    longitude NUMERIC(12,10),
    latitude NUMERIC(12,10),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_unit_peternak_pkey PRIMARY KEY(id)
);
