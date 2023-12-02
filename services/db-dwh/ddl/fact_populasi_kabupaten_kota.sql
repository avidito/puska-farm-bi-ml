-- Table
CREATE TABLE fact_populasi_kabupaten_kota (
    provinsi VARCHAR(100),
    kabupaten_kota VARCHAR(100),
    year INT8,
    populasi INT8,
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT fact_populasi_kabupaten_kota_pkey PRIMARY KEY(provinsi, kabupaten_kota, year)
);


-- Injection
CREATE TABLE tmp_populasi_kabupaten_kota (
    provinsi VARCHAR(100),
    kabupaten_kota VARCHAR(100),
    year_2009 INT8,
    year_2010 INT8,
    year_2011 INT8,
    year_2012 INT8,
    year_2013 INT8,
    year_2014 INT8,
    year_2015 INT8,
    year_2016 INT8,
    year_2017 INT8,
    year_2018 INT8,
    year_2019 INT8,
    year_2020 INT8,
    year_2021 INT8,
    year_2022 INT8,
    CONSTRAINT tmp_populasi_kabupaten_kota_pkey PRIMARY KEY (provinsi, kabupaten_kota)
);

COPY tmp_populasi_kabupaten_kota
FROM '/seed/populasi_kabupaten_kota.csv'
WITH (FORMAT 'csv', DELIMITER ';', HEADER TRUE);

INSERT INTO fact_populasi_kabupaten_kota (
    provinsi,
    kabupaten_kota,
    year,
    populasi,
    created_dt,
    modified_dt
)
SELECT
    provinsi,
    kabupaten_kota,
    year,
    populasi,
    CURRENT_TIMESTAMP AS created_dt,
    CURRENT_TIMESTAMP AS modified_dt
FROM (
    SELECT provinsi, kabupaten_kota, 2009 AS year, year_2009 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2010 AS year, year_2010 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2011 AS year, year_2011 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2012 AS year, year_2012 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2013 AS year, year_2013 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2014 AS year, year_2014 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2015 AS year, year_2015 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2016 AS year, year_2016 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2017 AS year, year_2017 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2018 AS year, year_2018 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2019 AS year, year_2019 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2020 AS year, year_2020 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2021 AS year, year_2021 AS populasi FROM tmp_populasi_kabupaten_kota
    UNION ALL SELECT provinsi, kabupaten_kota, 2022 AS year, year_2022 AS populasi FROM tmp_populasi_kabupaten_kota
) AS ud;

DROP TABLE tmp_populasi_kabupaten_kota;