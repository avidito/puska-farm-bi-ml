WITH cte_provinsi AS (
  SELECT
    id,
    kode,
    nama AS provinsi,
    NULL AS kabupaten_kota
  FROM wilayah
  WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 0
),
cte_kabupaten_kota AS (
  SELECT
    kk.id,
    kk.kode,
    p.provinsi,
    (CASE
      WHEN kk.kabupaten_kota = 'KEP. SERIBU' THEN 'KEPULAUAN SERIBU'
      ELSE kk.kabupaten_kota
    END) AS kabupaten_kota
  FROM (
    SELECT
      w.id,
      w.kode,
      (REGEXP_MATCH(w.kode, '^[0-9]+(?=\.)'))[1] AS prov_kode,
      REPLACE(REGEXP_REPLACE(w.nama, '(KAB.|KOTA) ', ''), 'ADM. ', '') AS kabupaten_kota
    FROM wilayah AS w
    WHERE LENGTH(REGEXP_REPLACE(kode, '[^.]', '', 'g')) = 1
  ) AS kk
    LEFT JOIN cte_provinsi AS p
      ON kk.prov_kode = p.kode
)
SELECT
  id,
  provinsi,
  kabupaten_kota
FROM (
  SELECT id, provinsi, NULL AS kabupaten_kota FROM cte_provinsi
  UNION ALL 
  SELECT id, provinsi, kabupaten_kota FROM cte_kabupaten_kota
) AS ud
UNION ALL
SELECT 999 AS id, '' AS provinsi, '' AS kabupaten_kota;
