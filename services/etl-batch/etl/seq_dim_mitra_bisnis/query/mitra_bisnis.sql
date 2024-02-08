SELECT
  mb.id,
  mb.id_unit_ternak AS id_unit_peternak,
  mb.nama_mitra AS nama_mitra_bisnis,
  km.nama_kategori AS kategori_mitra_bisnis
FROM mitra_bisnis AS mb
JOIN kategori_mitra AS km
  ON mb.id_kategori_mitra = km.id;