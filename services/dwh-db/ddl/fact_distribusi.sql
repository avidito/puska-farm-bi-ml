CREATE TABLE fact_distribusi (
    id_unit_ternak INT8,
    id_mitra_bisnis INT8,
    id_jenis_produk INT8,
    tanggal DATE,
    jumlah_distribusi INT8,
    harga_minimum INT8,
    harga_maximum INT8,
    harga_rata_rata NUMERIC(10,3),
    jumlah_penjualan INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_distribusi_pkey PRIMARY KEY(id_unit_ternak, id_mitra_bisnis, id_jenis_produk, tanggal)
);