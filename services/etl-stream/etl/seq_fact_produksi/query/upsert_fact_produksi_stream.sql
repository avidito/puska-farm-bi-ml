INSERT INTO fact_produksi_stream (
  id_waktu,
  id_lokasi,
  id_unit_ternak,
  id_jenis_produk,
  id_sumber_pasokan,
  jumlah_produksi,
  created_dt,
  modified_dt
)
VALUES (
  :id_waktu,
  :id_lokasi,
  :id_unit_ternak,
  :id_jenis_produk,
  :id_sumber_pasokan,
  :jumlah_produksi,
  CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta',
  CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'
)
ON CONFLICT (id_waktu, id_lokasi, id_unit_ternak, id_jenis_produk, id_sumber_pasokan)
DO UPDATE SET
  jumlah_produksi = excluded.jumlah_produksi,
  modified_dt = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta';