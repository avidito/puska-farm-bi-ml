SELECT
  id,
  kelurahan_id AS id_lokasi,
  nama_unit,
  alamat,
  NULL AS longitude,
  NULL AS latitude
FROM unit_ternak AS ut
UNION ALL
SELECT
  999 AS id,
  '999' AS id_lokasi,
  '' AS nama_unit,
  '' AS alamat,
  NULL AS longitude,
  NULL AS latitude;