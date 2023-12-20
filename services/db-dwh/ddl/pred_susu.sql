CREATE TABLE pred_susu (
    id_waktu INT8,
    id_lokasi INT8,
    id_unit_ternak INT8,
	prediction NUMERIC(10, 2),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP
);