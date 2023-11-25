WITH cte_produksi_susu AS (
  SELECT
    tgl_produksi AS tanggal,
    id_unit_ternak,
    sumber_pasokan,
    id_jenis_produk,
    jumlah AS jumlah_produksi
  FROM produksi_susu
),
cte_produksi_ternak AS (
  SELECT
    tgl_produksi AS tanggal,
    id_unit_ternak,
    sumber_pasokan,
    id_jenis_produk,
    jumlah AS jumlah_produksi
  FROM produksi_ternak
),
cte_union_produksi AS (
  SELECT tanggal, id_unit_ternak, sumber_pasokan, id_jenis_produk, jumlah_produksi FROM cte_produksi_susu UNION ALL
  SELECT tanggal, id_unit_ternak, sumber_pasokan, id_jenis_produk, jumlah_produksi FROM cte_produksi_ternak
),
cte_sumber_pasokan AS (
  SELECT
      ROW_NUMBER() OVER(ORDER BY nama_sumber_pasokan) AS id,
      nama_sumber_pasokan
    FROM (
      SELECT DISTINCT
        sumber_pasokan AS nama_sumber_pasokan
      FROM produksi_susu
    ) AS sp
)
SELECT
  p.id_unit_ternak,
  sp.id AS id_sumber_pasokan,
  p.id_jenis_produk,
  p.tanggal,
  SUM(p.jumlah_produksi) AS jumlah_produksi
FROM cte_union_produksi AS p
JOIN cte_sumber_pasokan AS sp
  ON p.sumber_pasokan = sp.nama_sumber_pasokan
GROUP BY 1, 2, 3, 4;