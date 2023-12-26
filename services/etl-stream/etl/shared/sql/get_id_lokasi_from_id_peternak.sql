SELECT ut.id_lokasi AS id_lokasi
FROM dim_peternakan AS mp
JOIN dim_unit_ternak AS ut
  ON mp.id_unit_ternak = ut.id
WHERE TRUE
  AND mp.id = :id_peternak;
