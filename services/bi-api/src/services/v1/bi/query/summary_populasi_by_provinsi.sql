WITH base AS (
  SELECT
    id_lokasi,
    jenis_kelamin,
    tipe_ternak,
    tipe_usia,
    SUM(jumlah) AS jumlah
  FROM fact_populasi
  GROUP BY 1, 2, 3, 4
),
cte_summary AS (
    SELECT
    l.provinsi,
    l.kabupaten_kota,
    SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahDewasaJantan,
    SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahDewasaBetina,
    SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahAnakanJantan,
    SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Perah' THEN jumlah END)) AS perahAnakanBetina,
    SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingDewasaJantan,
    SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingDewasaBetina,
    SUM((CASE WHEN jenis_kelamin = 'Jantan' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingAnakanJantan,
    SUM((CASE WHEN jenis_kelamin = 'Betina' AND tipe_ternak = 'Pedaging' THEN jumlah END)) AS pedagingAnakanBetina
    FROM base AS b
    LEFT JOIN dim_lokasi AS l
        ON b.id_lokasi = l.id
    GROUP BY 1, 2
)
SELECT
    provinsi,
    SUM(perahDewasaJantan) AS perahDewasaJantan,
    SUM(perahDewasaBetina) AS perahDewasaBetina,
    SUM(perahAnakanJantan) AS perahAnakanJantan,
    SUM(perahAnakanBetina) AS perahAnakanBetina,
    SUM(pedagingDewasaJantan) AS pedagingDewasaJantan,
    SUM(pedagingDewasaBetina) AS pedagingDewasaBetina,
    SUM(pedagingAnakanJantan) AS pedagingAnakanJantan,
    SUM(pedagingAnakanBetina) AS pedagingAnakanBetina
FROM cte_summary
GROUP BY 1;