WITH cte_pop_jantan_pedaging AS (
  SELECT
    COALESCE(hkk.tgl_pencatatan, ptm.tgl_pencatatan, ptk.tgl_pencatatan) AS tanggal,
    COALESCE(hkk.id_peternak, ptm.id_peternak, ptk.id_peternak) AS id_peternakan,
    'Jantan' AS jenis_kelamin,
    'Pedaging' AS tipe_ternak,
    COALESCE(SUM(hkk.jml_lahir_pedaging_jantan), 0) AS jumlah_lahir,
    COALESCE(SUM((hkk.jml_mati_pedaging_jantan + hkk.jml_mati_pedaging_anakan_jantan)), 0) AS jumlah_mati,
    COALESCE(SUM((ptm.jml_pedaging_jantan + ptm.jml_pedaging_anakan_jantan)), 0) AS jumlah_masuk,
    COALESCE(SUM((ptk.jml_pedaging_jantan + ptk.jml_pedaging_anakan_jantan)), 0) AS jumlah_keluar
  FROM history_kelahiran_kematian AS hkk
  FULL JOIN pencatatan_ternak_masuk AS ptm
    ON hkk.tgl_pencatatan = ptm.tgl_pencatatan
    AND hkk.id_peternak = ptm.id_peternak
  FULL JOIN pencatatan_ternak_keluar AS ptk
    ON hkk.tgl_pencatatan = ptk.tgl_pencatatan
    AND hkk.id_peternak = ptk.id_peternak
  GROUP BY 1, 2, 3, 4
),
cte_pop_betina_pedaging AS (
  SELECT
    COALESCE(hkk.tgl_pencatatan, ptm.tgl_pencatatan, ptk.tgl_pencatatan) AS tanggal,
    COALESCE(hkk.id_peternak, ptm.id_peternak, ptk.id_peternak) AS id_peternakan,
    'Betina' AS jenis_kelamin,
    'Pedaging' AS tipe_ternak,
    COALESCE(SUM(hkk.jml_lahir_pedaging_betina), 0) AS jumlah_lahir,
    COALESCE(SUM((hkk.jml_mati_pedaging_betina + hkk.jml_mati_pedaging_anakan_betina)), 0) AS jumlah_mati,
    COALESCE(SUM((ptm.jml_pedaging_betina + ptm.jml_pedaging_anakan_betina)), 0) AS jumlah_masuk,
    COALESCE(SUM((ptk.jml_pedaging_betina + ptk.jml_pedaging_anakan_betina)), 0) AS jumlah_keluar
  FROM history_kelahiran_kematian AS hkk
  FULL JOIN pencatatan_ternak_masuk AS ptm
    ON hkk.tgl_pencatatan = ptm.tgl_pencatatan
    AND hkk.id_peternak = ptm.id_peternak
  FULL JOIN pencatatan_ternak_keluar AS ptk
    ON hkk.tgl_pencatatan = ptk.tgl_pencatatan
    AND hkk.id_peternak = ptk.id_peternak
  GROUP BY 1, 2, 3, 4
),
cte_pop_jantan_perah AS (
  SELECT
    COALESCE(hkk.tgl_pencatatan, ptm.tgl_pencatatan, ptk.tgl_pencatatan) AS tanggal,
    COALESCE(hkk.id_peternak, ptm.id_peternak, ptk.id_peternak) AS id_peternakan,
    'Jantan' AS jenis_kelamin,
    'Perah' AS tipe_ternak,
    COALESCE(SUM(hkk.jml_lahir_perah_jantan), 0) AS jumlah_lahir,
    COALESCE(SUM((hkk.jml_mati_perah_jantan + hkk.jml_mati_perah_anakan_jantan)), 0) AS jumlah_mati,
    COALESCE(SUM((ptm.jml_perah_jantan + ptm.jml_perah_anakan_jantan)), 0) AS jumlah_masuk,
    COALESCE(SUM((ptk.jml_perah_jantan + ptk.jml_perah_anakan_jantan)), 0) AS jumlah_keluar
  FROM history_kelahiran_kematian AS hkk
  FULL JOIN pencatatan_ternak_masuk AS ptm
    ON hkk.tgl_pencatatan = ptm.tgl_pencatatan
    AND hkk.id_peternak = ptm.id_peternak
  FULL JOIN pencatatan_ternak_keluar AS ptk
    ON hkk.tgl_pencatatan = ptk.tgl_pencatatan
    AND hkk.id_peternak = ptk.id_peternak
  GROUP BY 1, 2, 3, 4
),
cte_pop_betina_perah AS (
  SELECT
    COALESCE(hkk.tgl_pencatatan, ptm.tgl_pencatatan, ptk.tgl_pencatatan) AS tanggal,
    COALESCE(hkk.id_peternak, ptm.id_peternak, ptk.id_peternak) AS id_peternakan,
    'Betina' AS jenis_kelamin,
    'Perah' AS tipe_ternak,
    COALESCE(SUM(hkk.jml_lahir_perah_betina), 0) AS jumlah_lahir,
    COALESCE(SUM((hkk.jml_mati_perah_betina + hkk.jml_mati_perah_anakan_betina)), 0) AS jumlah_mati,
    COALESCE(SUM((ptm.jml_perah_betina + ptm.jml_perah_anakan_betina)), 0) AS jumlah_masuk,
    COALESCE(SUM((ptk.jml_perah_betina + ptk.jml_perah_anakan_betina)), 0) AS jumlah_keluar
  FROM history_kelahiran_kematian AS hkk
  FULL JOIN pencatatan_ternak_masuk AS ptm
    ON hkk.tgl_pencatatan = ptm.tgl_pencatatan
    AND hkk.id_peternak = ptm.id_peternak
  FULL JOIN pencatatan_ternak_keluar AS ptk
    ON hkk.tgl_pencatatan = ptk.tgl_pencatatan
    AND hkk.id_peternak = ptk.id_peternak
  GROUP BY 1, 2, 3, 4
),
cte_populasi AS (
  SELECT
    ud.tanggal,
    ut.kota_id AS id_lokasi,
    ut.id AS id_unit_ternak,
    ud.jenis_kelamin,
    ud.tipe_ternak,
    SUM(ud.jumlah_lahir) AS jumlah_lahir,
    SUM(ud.jumlah_mati) AS jumlah_mati,
    SUM(ud.jumlah_masuk) AS jumlah_masuk,
    SUM(ud.jumlah_keluar) AS jumlah_keluar,
    SUM((ud.jumlah_lahir + ud.jumlah_masuk) - (ud.jumlah_mati + ud.jumlah_keluar)) AS jumlah
  FROM (
    SELECT tanggal, id_peternakan, jenis_kelamin, tipe_ternak, jumlah_lahir, jumlah_mati, jumlah_masuk, jumlah_keluar FROM cte_pop_jantan_pedaging UNION ALL
    SELECT tanggal, id_peternakan, jenis_kelamin, tipe_ternak, jumlah_lahir, jumlah_mati, jumlah_masuk, jumlah_keluar FROM cte_pop_betina_pedaging UNION ALL
    SELECT tanggal, id_peternakan, jenis_kelamin, tipe_ternak, jumlah_lahir, jumlah_mati, jumlah_masuk, jumlah_keluar FROM cte_pop_jantan_perah UNION ALL
    SELECT tanggal, id_peternakan, jenis_kelamin, tipe_ternak, jumlah_lahir, jumlah_mati, jumlah_masuk, jumlah_keluar FROM cte_pop_betina_perah
  ) AS ud
  JOIN mitra_peternak AS mp
    ON ud.id_peternakan = mp.id
  JOIN unit_ternak AS ut
    ON mp.id_unit_ternak = ut.id
  GROUP BY 1, 2, 3, 4, 5
)
SELECT
  tanggal,
  id_lokasi,
  id_unit_ternak AS id_unit_peternak,
  jenis_kelamin,
  tipe_ternak,
  '' AS tipe_usia,
  jumlah_lahir,
  jumlah_mati,
  jumlah_masuk,
  jumlah_keluar,
  jumlah
FROM cte_populasi;
