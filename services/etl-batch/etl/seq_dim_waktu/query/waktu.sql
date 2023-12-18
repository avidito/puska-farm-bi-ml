WITH cte_lama AS (
  SELECT tahun
  FROM GENERATE_SERIES(2009, 2022) AS tahun
),
cte_baru AS (
  SELECT
    DATE_PART('year', dt) AS tahun,
    DATE_PART('month', dt) AS bulan,
    DATE_PART('week', dt) AS minggu,
    DATE_PART('day', dt) AS tanggal
  FROM (
    SELECT dt::date
    FROM GENERATE_SERIES(
      '2023-01-01',
      '2027-12-31',
      INTERVAL '1 DAY'
    ) AS dt
  ) AS gen_dt
)
SELECT
  ROW_NUMBER() OVER (ORDER BY tahun, bulan, minggu, tanggal) AS id,
  tahun,
  bulan,
  minggu,
  tanggal
FROM (
  SELECT tahun, NULL AS bulan, NULL AS minggu, NULL AS tanggal FROM cte_lama
  UNION ALL
  SELECT tahun, bulan, minggu, tanggal FROM cte_baru
) AS ud
ORDER BY 1;
