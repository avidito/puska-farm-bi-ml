import logging
import pydantic
from typing import Type, Union
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

##### CREATE #####
# Indented
{
    "source_table": "produksi_susu",
    "action": "CREATE",
    "identifier": {
        "tgl_produksi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_jenis_produk": 1,
        "sumber_pasokan": "Pengepul"
    },
    "amount": {
        "jumlah": 10000
    }
}

# Flatten
{"source_table": "produksi", "action": "CREATE", "identifier": {"tgl_produksi": "2023-12-23", "id_unit_ternak": 1, "id_jenis_produk": 1, "sumber_pasokan": "Pengepul"}, "amount": {"jumlah": 10000}}

##### DELETE #####
# Indented
{
    "source_table": "produksi_susu",
    "action": "DELETE",
    "identifier": {
        "tgl_produksi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_jenis_produk": 1,
        "sumber_pasokan": "Pengepul"
    },
    "amount": {
        "jumlah": 10000
    }
}

# Flatten
{"source_table": "produksi_susu", "action": "DELETE", "identifier": {"tgl_produksi": "2023-12-23", "id_unit_ternak": 1, "id_jenis_produk": 1, "sumber_pasokan": "Pengepul"}, "amount": {"jumlah": 10000}}

##### UPDATE #####
# Indented
{
    "source_table": "produksi_susu",
    "action": "UPDATE",
    "identifier": {
        "tgl_produksi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_jenis_produk": 1,
        "sumber_pasokan": "Pengepul"
    },
    "amount": {
        "jumlah": 8000,
        "prev_jumlah": 10000
    }
}

# Flatten
{"source_table": "produksi_susu", "action": "UPDATE", "identifier": {"tgl_produksi": "2023-12-23", "id_unit_ternak": 1, "id_jenis_produk": 1, "sumber_pasokan": "Pengepul"}, "amount": {"jumlah": 8000, "prev_jumlah": 10000}}

"""
# Event
class IdentifierFactProduksi(pydantic.BaseModel):
    tgl_produksi: date
    id_unit_ternak: int
    id_jenis_produk: int
    sumber_pasokan: str

class AmountFactProduksi(pydantic.BaseModel):
    jumlah: int

class AmountUpdateFactProduksi(pydantic.BaseModel):
    jumlah: int
    prev_jumlah: int

class EventFactProduksi(pydantic.BaseModel):
    source_table: str
    action: str
    identifier: IdentifierFactProduksi
    amount: Union[AmountUpdateFactProduksi, AmountFactProduksi]

# Table
class TableFactProduksi(pydantic.BaseModel):
    id_waktu: int
    id_lokasi: int
    id_unit_ternak: int
    id_jenis_produk: int
    id_sumber_pasokan: int
    jumlah_produksi: int
