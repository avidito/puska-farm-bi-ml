CREATE TABLE dim_peternakan (
    id INT8,
    id_unit_ternak INT8,
    nama_peternakan VARCHAR(100),
    nama_pemilik VARCHAR(100),
    jenis_kelamin VARCHAR(10),
    tgl_lahir DATE,
    pendidikan VARCHAR(30),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_peternakan_pkey PRIMARY KEY(id)
);