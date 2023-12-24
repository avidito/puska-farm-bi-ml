SELECT
  id_waktu,
  id_lokasi,
  id_unit_ternak,
  id_jenis_produk,
  id_sumber_pasokan,
  jumlah_produksi
FROM fact_produksi_stream
WHERE TRUE
  AND id_waktu = :id_waktu
  AND id_lokasi = :id_lokasi
  AND id_unit_ternak = :id_unit_ternak
  AND id_jenis_produk = :id_jenis_produk
  AND id_sumber_pasokan = :id_sumber_pasokan;
