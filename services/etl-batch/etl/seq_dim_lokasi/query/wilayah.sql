WITH provinsi AS (
  SELECT
    kode AS kode_provinsi,
    nama
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 0
),
kabupaten_kota AS (
  SELECT
    SPLIT_PART(kode, '.', 2) AS kode_kabupaten_kota,
    REGEXP_REPLACE(nama, '(KAB.|KOTA) ', '') AS nama
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 1
),
kecamatan AS (
  SELECT
    SPLIT_PART(kode, '.', 2) AS kode_kecamatan,
    UPPER(nama) AS nama
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 2
),
desa_kelurahan AS (
  SELECT
    id,
    SPLIT_PART(kode, '.', 1) AS kode_provinsi,
    SPLIT_PART(kode, '.', 2) AS kode_kabupaten_kota,
    SPLIT_PART(kode, '.', 3) AS kode_kecamatan,
    UPPER(nama) AS nama
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 3
)
SELECT
  kel.id,
  p.nama AS provinsi,
  kk.nama AS kabupaten_kota,
  kec.nama AS kecamatan,
  kel.nama AS desa_kelurahan
FROM desa_kelurahan AS kel
JOIN kecamatan AS kec
  ON kel.kode_kecamatan = kec.kode_kecamatan
JOIN kabupaten_kota AS kk
  ON kel.kode_kabupaten_kota = kk.kode_kabupaten_kota
JOIN provinsi AS p
  ON kel.kode_provinsi = p.kode_provinsi