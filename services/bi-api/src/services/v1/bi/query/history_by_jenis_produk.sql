WITH prd AS (
  SELECT
      id_waktu,
      SUM(jumlah_produksi) AS totalProduksi
  FROM fact_produksi
  WHERE id_jenis_produk = {{ id_jenis_produk }}
  GROUP BY 1
),
dst AS (
  SELECT
    id_waktu,
    SUM(jumlah_distribusi) AS totalDistribusi
  FROM fact_distribusi
  WHERE id_jenis_produk = {{ id_jenis_produk }}
  GROUP BY 1
),
cte_summary AS (
  SELECT
    COALESCE(p.id_waktu, d.id_waktu) AS id_waktu,
    COALESCE(p.totalProduksi, 0) AS totalProduksi,
    COALESCE(d.totalDistribusi, 0) AS totalDistribusi
  FROM prd AS p
  FULL JOIN dst AS d
    ON p.id_waktu = d.id_waktu
)
SELECT
  TO_DATE(
    CONCAT(w.tahun, '-', LPAD(w.bulan::varchar, 2, '0'), '-', LPAD(w.tanggal::varchar, 2, '0')),
    'YYYY-MM-DD'
  ) AS "date",
  s.totalProduksi,
  s.totalDistribusi
FROM cte_summary AS s
JOIN dim_waktu AS w
  ON s.id_waktu = w.id
ORDER BY 1;