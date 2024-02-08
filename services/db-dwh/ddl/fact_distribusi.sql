-- Table: Batch
CREATE TABLE fact_distribusi (
    id_waktu INT8,
    id_lokasi INT8,
    id_unit_peternak INT8,
    id_mitra_bisnis INT8,
    id_jenis_produk INT8,
    jumlah_distribusi INT8,
    harga_minimum INT8,
    harga_maximum INT8,
    harga_rata_rata NUMERIC(10,3),
    jumlah_penjualan INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_distribusi_pkey PRIMARY KEY(id_waktu, id_lokasi, id_unit_peternak, id_mitra_bisnis, id_jenis_produk)
);

-- Table: Stream
CREATE TABLE fact_distribusi_stream (
    id_waktu INT8,
    id_lokasi INT8,
    id_unit_peternak INT8,
    id_mitra_bisnis INT8,
    id_jenis_produk INT8,
    jumlah_distribusi INT8,
    harga_minimum INT8,
    harga_maximum INT8,
    harga_rata_rata NUMERIC(10,3),
    jumlah_penjualan INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_distribusi_stream_pkey PRIMARY KEY(id_waktu, id_lokasi, id_unit_peternak, id_mitra_bisnis, id_jenis_produk)
);
