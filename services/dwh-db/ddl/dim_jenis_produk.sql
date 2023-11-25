CREATE TABLE dim_jenis_produk (
    id INT8,
    nama_produk VARCHAR(100),
    kategori_produk VARCHAR(100),
    satuan VARCHAR(100),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_jenis_produk_pkey PRIMARY KEY (id)
);