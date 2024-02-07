WITH prd AS (
  SELECT
      id_jenis_produk AS idJenisProduk,
      SUM(jumlah_produksi) AS totalProduksi
  FROM fact_produksi
  GROUP BY 1
),
dst AS (
  SELECT
    id_jenis_produk AS idJenisProduk,
    SUM(jumlah_distribusi) AS totalDistribusi
  FROM fact_distribusi
  GROUP BY 1
),
cte_summary AS (
  SELECT
    COALESCE(p.idJenisProduk, d.idJenisProduk) AS idJenisProduk,
    COALESCE(p.totalProduksi) AS totalProduksi,
    COALESCE(d.totalDistribusi) AS totalDistribusi
  FROM prd AS p
  FULL JOIN dst AS d
    ON p.idJenisProduk = d.idJenisProduk
)
SELECT
  idJenisProduk,
  totalProduksi,
  totalDistribusi,
  COALESCE(totalDistribusi / NULLIF(totalProduksi, 0), 0) AS persentase
FROM cte_summary
ORDER BY 1;