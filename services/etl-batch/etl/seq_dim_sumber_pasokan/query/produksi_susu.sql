SELECT
  ROW_NUMBER() OVER(ORDER BY nama_sumber_pasokan) AS id,
  nama_sumber_pasokan
FROM (
  SELECT DISTINCT
    sumber_pasokan AS nama_sumber_pasokan
  FROM produksi_susu
) AS sp;