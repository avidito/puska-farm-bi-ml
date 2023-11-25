CREATE TABLE dim_lokasi (
    id INT8,
    provinsi VARCHAR(100),
    kabupaten_kota VARCHAR(100),
    kecamatan VARCHAR(100),
    desa_kelurahan VARCHAR(100),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_lokasi_pkey PRIMARY KEY(id)
);