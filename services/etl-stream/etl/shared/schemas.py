import logging
import pydantic
from typing import Type
from datetime import date


# Validation
def validating_event(data: dict, Base: Type[pydantic.BaseModel], logger: logging.Logger) -> pydantic.BaseModel:
    try:
        return Base(**data)
    except pydantic.ValidationError as err:
        logger.error(str(err))
        raise(err)


# Schemas - Produksi
"""
JSON Sample:
{
    "source_table": "produksi",
    "data": {
        "tgl_produksi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_jenis_produk": 1,
        "sumber_pasokan": "Pengepul",
        "jumlah": 10000
    }
}

Input for Kafka Producer Console (flatten):
{"source_table": "produksi", "data": {"tgl_produksi": "2023-12-23", "id_unit_ternak": 1, "id_jenis_produk": 1, "sumber_pasokan": "Pengepul", "jumlah": 10000}}
{"source_table": "produksi", "data": {"tgl_produksi": "2023-12-23", "id_unit_ternak": 1, "id_jenis_produk": 1, "sumber_pasokan": "Pengepul", "jumlah": -10000}}
"""
class DataProduksi(pydantic.BaseModel):
    tgl_produksi: date
    id_unit_ternak: int
    id_jenis_produk: int
    sumber_pasokan: str
    jumlah: int

class EventFactProduksi(pydantic.BaseModel):
    source_table: str
    data: DataProduksi

class TableFactProduksi(pydantic.BaseModel):
    id_waktu: int
    id_lokasi: int
    id_unit_ternak: int
    id_jenis_produk: int
    id_sumber_pasokan: int
    jumlah_produksi: int