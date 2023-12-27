SELECT id AS id_waktu
FROM dim_waktu
WHERE TRUE
  AND tahun = :tahun
  AND bulan = :bulan
  AND tanggal = :tanggal