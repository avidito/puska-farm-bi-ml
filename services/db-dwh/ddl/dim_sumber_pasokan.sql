-- Table
CREATE TABLE dim_sumber_pasokan (
    id SERIAL,
    nama_sumber_pasokan VARCHAR(100),
    created_dt TIMESTAMP,
    modified_dt TIMESTAMP,
    CONSTRAINT dim_sumber_pasokan_pkey PRIMARY KEY(id)
);
