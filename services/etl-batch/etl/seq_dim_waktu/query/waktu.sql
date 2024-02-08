WITH cte_lama AS (
  SELECT tahun
  FROM GENERATE_SERIES(2009, 2022) AS tahun
),
cte_baru AS (
  SELECT
    dt AS tanggal,
    DATE_PART('year', dt) AS tahun,
    DATE_PART('month', dt) AS bulan,
    DATE_PART('day', dt) AS hari
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
  ROW_NUMBER() OVER (ORDER BY tanggal) AS id,
  tanggal,
  tahun,
  bulan,
  hari
FROM (
  SELECT NULL AS tanggal, tahun, NULL AS bulan, NULL AS hari FROM cte_lama
  UNION ALL
  SELECT tanggal, tahun, bulan, hari FROM cte_baru
) AS ud
ORDER BY 1;
