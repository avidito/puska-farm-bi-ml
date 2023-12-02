-- Table
CREATE TABLE kategori_mitra (
	id BIGSERIAL,
	nama_kategori VARCHAR(255),
	CONSTRAINT kategori_mitra_pkey PRIMARY KEY (id)
);

-- Inject
COPY kategori_mitra
FROM '/seed/kategori_mitra.csv'
WITH (FORMAT 'csv', DELIMITER ',', HEADER TRUE, NULL 'NULL', QUOTE "'");
