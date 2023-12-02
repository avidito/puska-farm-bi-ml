-- Table
CREATE TABLE fact_produksi (
    id_unit_ternak INT8,
    id_sumber_pasokan INT8,
    id_jenis_produk INT8,
    tanggal DATE,
    jumlah_produksi INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_produksi_pkey PRIMARY KEY(id_unit_ternak, id_sumber_pasokan, id_jenis_produk, tanggal)
);
