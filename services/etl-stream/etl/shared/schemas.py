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


"""
Schemas - Produksi
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


"""
Schemas - Distribusi
JSON Sample:

##### CREATE #####
# Indented
{
    "source_table": "distribusi_susu",
    "action": "CREATE",
    "identifier": {
        "tgl_distribusi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_lokasi": 27696,
        "id_mitra_bisnis": 1,
        "id_jenis_produk": 1
    },
    "amount": {
        "jumlah": 10000,
        "harga_berlaku": 2000
    }
}

# Flatten
{"source_table": "distribusi_susu", "action": "CREATE", "identifier": {"tgl_distribusi": "2023-12-23", "id_unit_ternak": 1, "id_lokasi": 27696, "id_mitra_bisnis": 1, "id_jenis_produk": 1}, "amount": {"jumlah": 10000, "harga_berlaku": 2000}}

##### DELETE #####
# Indented
{
    "source_table": "distribusi_susu",
    "action": "DELETE",
    "identifier": {
        "tgl_distribusi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_lokasi": 27696,
        "id_mitra_bisnis": 1,
        "id_jenis_produk": 1
    },
    "amount": {
        "jumlah": 10000,
        "harga_berlaku": 2000
    }
}

# Flatten
{"source_table": "distribusi_susu", "action": "DELETE", "identifier": {"tgl_distribusi": "2023-12-23", "id_unit_ternak": 1, "id_lokasi": 27696, "id_mitra_bisnis": 1, "id_jenis_produk": 1}, "amount": {"jumlah": 10000, "harga_berlaku": 2000}}

##### UPDATE #####
# Indented
{
    "source_table": "distribusi_susu",
    "action": "UPDATE",
    "identifier": {
        "tgl_distribusi": "2023-12-23",
        "id_unit_ternak": 1,
        "id_lokasi": 27696,
        "id_mitra_bisnis": 1,
        "id_jenis_produk": 1
    },
    "amount": {
        "jumlah": 8000,
        "harga_berlaku": 2500,
        "prev_jumlah": 10000,
        "prev_harga_berlaku": 2000
    }
}

# Flatten
{"source_table": "distribusi_susu", "action": "UPDATE", "identifier": {"tgl_distribusi": "2023-12-23", "id_unit_ternak": 1, "id_lokasi": 27696, "id_mitra_bisnis": 1, "id_jenis_produk": 1}, "amount": {"jumlah": 8000, "harga_berlaku": 2500, "prev_jumlah": 10000, "prev_harga_berlaku": 2000}}

"""

# Event
class IdentifierFactDistribusi(pydantic.BaseModel):
    tgl_distribusi: date
    id_unit_ternak: int
    id_lokasi: int
    id_mitra_bisnis: int
    id_jenis_produk: int

class AmountFactDistribusi(pydantic.BaseModel):
    jumlah: int
    harga_berlaku: int

class AmountUpdateFactDistribusi(pydantic.BaseModel):
    jumlah: int
    harga_berlaku: int
    prev_jumlah: int
    prev_harga_berlaku: int

class EventFactDistribusi(pydantic.BaseModel):
    source_table: str
    action: str
    identifier: IdentifierFactDistribusi
    amount: Union[AmountUpdateFactDistribusi, AmountFactDistribusi]

# Table
class TableFactDistribusi(pydantic.BaseModel):
    id_waktu: int
    id_lokasi: int
    id_unit_ternak: int
    id_mitra_bisnis: int
    id_jenis_produk: int
    jumlah_distribusi: int
    jumlah_penjualan: int
