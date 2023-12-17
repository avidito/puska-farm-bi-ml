SELECT
  id,
  kelurahan_id AS id_lokasi,
  nama_unit,
  alamat,
  NULL AS longitude,
  NULL AS latitude
FROM unit_ternak AS ut;