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
  id_unit_ternak,
  id_mitra_bisnis,
  id_jenis_produk,
  tanggal,
  SUM(jumlah_distribusi) AS jumlah_distribusi,
  MIN(harga) AS harga_minimum,
  MAX(harga) AS harga_maximum,
  AVG(harga) AS harga_rata_rata,
  SUM(jumlah_penjualan) AS jumlah_penjualan
FROM cte_union_distribusi
GROUP BY 1, 2, 3, 4;