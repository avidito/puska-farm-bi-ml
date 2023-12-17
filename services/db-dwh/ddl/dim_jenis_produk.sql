-- Table
CREATE TABLE dim_jenis_produk (
    id SERIAL,
    nama_produk VARCHAR(100),
    kategori_produk VARCHAR(100),
    satuan VARCHAR(100),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_jenis_produk_pkey PRIMARY KEY (id)
);
