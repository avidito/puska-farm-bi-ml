WITH cte_distribusi_susu AS (
  SELECT
    tgl_distribusi AS tanggal,
    id_unit_ternak,
    id_mitra_bisnis,
    id_jenis_produk,
    jumlah AS jumlah_distribusi,
    harga_berlaku AS harga,
    (jumlah * harga_berlaku) AS jumlah_penjualan
  FROM distribusi_susu
),
cte_distribusi_ternak AS (
  SELECT
    tgl_distribusi AS tanggal,
    id_unit_ternak,
    id_mitra_bisnis,
    id_jenis_produk,
    jumlah AS jumlah_distribusi,
    harga_berlaku AS harga,
    (jumlah * harga_berlaku) AS jumlah_penjualan
  FROM distribusi_ternak
),
cte_union_distribusi AS (
  SELECT tanggal, id_unit_ternak, id_mitra_bisnis, id_jenis_produk, jumlah_distribusi, harga, jumlah_penjualan FROM cte_distribusi_susu UNION ALL
  SELECT tanggal, id_unit_ternak, id_mitra_bisnis, id_jenis_produk, jumlah_distribusi, harga, jumlah_penjualan FROM cte_distribusi_ternak
)
SELECT
  ud.tanggal,
  ut.kota_id AS id_lokasi,
  ud.id_unit_ternak,
  ud.id_mitra_bisnis,
  ud.id_jenis_produk,
  SUM(ud.jumlah_distribusi) AS jumlah_distribusi,
  MIN(ud.harga) AS harga_minimum,
  MAX(ud.harga) AS harga_maximum,
  AVG(ud.harga) AS harga_rata_rata,
  SUM(ud.jumlah_penjualan) AS jumlah_penjualan
FROM cte_union_distribusi AS ud
JOIN unit_ternak AS ut
  ON ud.id_unit_ternak = ut.id
GROUP BY 1, 2, 3, 4, 5;