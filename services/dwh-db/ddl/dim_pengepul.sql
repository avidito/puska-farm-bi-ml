CREATE TABLE dim_pengepul (
    id INT8,
    id_unit_ternak INT8,
    nama_pengepul VARCHAR(100),
    jenis_pengepul VARCHAR(100),
    jenis_kelamin VARCHAR(10),
    tgl_lahir DATE,
    pendidikan VARCHAR(15),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_pengepul_pkey PRIMARY KEY(id)
);