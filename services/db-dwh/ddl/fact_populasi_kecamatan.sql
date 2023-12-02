-- Table
CREATE TABLE fact_populasi_kecamatan (
    provinsi VARCHAR(100),
    kabupaten_kota VARCHAR(100),
    kecamatan VARCHAR(100),
    year INT8,
    populasi INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_populasi_kecamatan_pkey PRIMARY KEY(provinsi, kabupaten_kota, kecamatan, year)
);


-- Injection
CREATE TABLE tmp_populasi_kecamatan (
    provinsi VARCHAR(100),
    kabupaten_kota VARCHAR(100),
    kecamatan VARCHAR(100),
    year_2018 INT8,
    year_2019 INT8,
    year_2020 INT8,
    year_2021 INT8,
    year_2022 INT8,
    CONSTRAINT tmp_populasi_kecamatan_pkey PRIMARY KEY (provinsi, kabupaten_kota, kecamatan)
);

COPY tmp_populasi_kecamatan
FROM '/seed/populasi_kecamatan.csv'
WITH (FORMAT 'csv', DELIMITER ';', HEADER TRUE);

INSERT INTO fact_populasi_kecamatan (
    provinsi,
    kabupaten_kota,
    kecamatan,
    year,
    populasi,
    created_dt,
    modified_dt
)
SELECT
    provinsi,
    kabupaten_kota,
    kecamatan,
    year,
    populasi,
    CURRENT_TIMESTAMP AS created_dt,
    CURRENT_TIMESTAMP AS modified_dt
FROM (
    SELECT provinsi, kabupaten_kota, kecamatan, 2018 AS year, year_2018 AS populasi FROM tmp_populasi_kecamatan
    UNION ALL SELECT provinsi, kabupaten_kota, kecamatan, 2019 AS year, year_2019 AS populasi FROM tmp_populasi_kecamatan
    UNION ALL SELECT provinsi, kabupaten_kota, kecamatan, 2020 AS year, year_2020 AS populasi FROM tmp_populasi_kecamatan
    UNION ALL SELECT provinsi, kabupaten_kota, kecamatan, 2021 AS year, year_2021 AS populasi FROM tmp_populasi_kecamatan
    UNION ALL SELECT provinsi, kabupaten_kota, kecamatan, 2022 AS year, year_2022 AS populasi FROM tmp_populasi_kecamatan
) AS ud;

DROP TABLE tmp_populasi_kecamatan;