-- Table
CREATE TABLE dim_waktu (
    id SERIAL,
    tahun INT8,
    bulan INT8,
    minggu INT8,
    tanggal INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_waktu_pk PRIMARY KEY(id)
);
