WITH base AS (
  SELECT
    jenis_kelamin,
    tipe_ternak,
    tipe_usia,
    SUM(jumlah) AS jumlah
  FROM fact_populasi
  GROUP BY 1, 2, 3
)
SELECT
  SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahDewasaJantan,
  SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahDewasaBetina,
  SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahAnakanJantan,
  SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahAnakanBetina,
  SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingDewasaJantan,
  SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingDewasaBetina,
  SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingAnakanJantan,
  SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingAnakanBetina
FROM base;