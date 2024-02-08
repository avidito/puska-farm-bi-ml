WITH cte_provinsi AS (
  SELECT
    id,
    kode,
    nama AS provinsi,
    NULL AS kabupaten_kota,
    NULL AS kecamatan 
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 0
),
cte_kabupaten_kota AS (
  SELECT
    kk.id,
    kk.kode,
    kk.prov_kode,
    kk.kabkota_kode,
    p.provinsi,
    (CASE
      WHEN kk.kabupaten_kota = 'KEP. SERIBU' THEN 'KEPULAUAN SERIBU'
      ELSE kk.kabupaten_kota
    END) AS kabupaten_kota,
    NULL AS kecamatan
  FROM (
    SELECT
      w.id,
      w.kode,
      SPLIT_PART(w.kode, '.', 1) AS prov_kode,
      SPLIT_PART(w.kode, '.', 2) AS kabkota_kode,
      REPLACE(REGEXP_REPLACE(w.nama, '(KAB.|KOTA) ', ''), 'ADM. ', '') AS kabupaten_kota
    FROM wilayah AS w
    WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 1
  ) AS kk
    LEFT JOIN cte_provinsi AS p
      ON kk.prov_kode = p.kode
),
cte_kecamatan AS (
  SELECT
    ke.id,
    ke.kode,
    ke.prov_kode,
    ke.kabkota_kode,
    p.provinsi,
    kk.kabupaten_kota,
    ke.kecamatan
  FROM (
    SELECT
      w.id,
      w.kode,
      SPLIT_PART(w.kode, '.', 1) AS prov_kode,
      SPLIT_PART(w.kode, '.', 2) AS kabkota_kode,
      UPPER(nama) AS kecamatan
    FROM wilayah AS w
    WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 2
  ) AS ke
    LEFT JOIN cte_provinsi AS p
      ON ke.prov_kode = p.kode
    LEFT JOIN cte_kabupaten_kota AS kk
      ON ke.prov_kode = kk.prov_kode
      AND ke.kabkota_kode = kk.kabkota_kode
)
SELECT
  ud.id,
  ud.provinsi,
  ud.kabupaten_kota,
  ud.kecamatan
FROM (
  SELECT id, provinsi, kabupaten_kota, kecamatan FROM cte_provinsi
  UNION ALL 
  SELECT id, provinsi, kabupaten_kota, kecamatan FROM cte_kabupaten_kota
  UNION ALL
  SELECT id, provinsi, kabupaten_kota, kecamatan FROM cte_kecamatan
) AS ud
UNION ALL
SELECT 999 AS id, '' AS provinsi, '' AS kabupaten_kota, '' AS kecamatan;
