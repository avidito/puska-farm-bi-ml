-- Table
CREATE TABLE fact_produksi (
    id_waktu INT8,
    id_lokasi INT8,
    id_unit_ternak INT8,
    id_jenis_produk INT8,
    id_sumber_pasokan INT8,
    jumlah_produksi INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_produksi_pkey PRIMARY KEY(id_waktu, id_lokasi, id_unit_ternak, id_jenis_produk, id_sumber_pasokan)
);
