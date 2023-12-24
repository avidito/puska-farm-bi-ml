SELECT ut.id_lokasi AS id_lokasi
FROM dim_unit_ternak AS ut
WHERE ut.id = :id_unit_ternak;