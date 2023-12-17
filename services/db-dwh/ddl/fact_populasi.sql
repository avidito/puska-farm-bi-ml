-- Table
CREATE TABLE fact_populasi (
    id_waktu INT8,
    id_unit_ternak INT8,
    jenis_kelamin VARCHAR(10),
    tipe_ternak VARCHAR(15),
    tipe_usia VARCHAR(15),
    jumlah_lahir INT8,
    jumlah_mati INT8,
    jumlah_masuk INT8,
    jumlah_keluar INT8,
    jumlah INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_populasi_pkey PRIMARY KEY(id_waktuid, _unit_ternak)
);
