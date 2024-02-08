from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime
from sqlalchemy.orm import declarative_base
Base  = declarative_base()

# Mixin
class LoadDtMixin:
    create_dt = Column(DateTime)
    modified_dt = Column(DateTime)


# Tables
# Dim
class DimJenisProduk(Base, LoadDtMixin):
    __tablename__ = "dim_jenis_produk"

    id = Column(Integer, primary_key=True)
    nama_produk = Column(String(255))
    kategori_produk = Column(String(255))
    satuan = Column(String(255))

class DimLokasi(Base, LoadDtMixin):
    __tablename__ = "dim_lokasi"

    id = Column(Integer, primary_key=True)
    provinsi = Column(String(255))
    kabupaten_kota = Column(String(255))
    kecamatan = Column(String(255))

class DimMitraBisnis(Base, LoadDtMixin):
    __tablename__ = "dim_mitra_bisnis"

    id = Column(Integer, primary_key=True)
    id_unit_peternak = Column(Integer)
    nama_mitra_bisnis = Column(String(20))
    kategori_mitra_bisnis = Column(String(255))

class DimPengepul(Base, LoadDtMixin):
    __tablename__ = "dim_pengepul"

    id = Column(Integer, primary_key=True)
    id_unit_peternak = Column(Integer)
    nama_pengepul = Column(String(255))
    jenis_pengepul = Column(String(255))
    jenis_kelamin = Column(String(255))
    tgl_lahir = Column(Date)
    pendidikan = Column(String(255))

class DimPeternakan(Base, LoadDtMixin):
    __tablename__ = "dim_peternakan"

    id = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer)
    nama_peternakan = Column(String(255))
    nama_pemilik = Column(String(255))
    jenis_kelamin = Column(String(255))
    tgl_lahir = Column(Date)
    pendidikan = Column(String(255))

class DimSumberPasokan(Base, LoadDtMixin):
    __tablename__ = "dim_sumber_pasokan"

    id = Column(Integer, primary_key=True)
    nama_sumber_pasokan = Column(String(255))

class DimUnitPeternak(Base, LoadDtMixin):
    __tablename__ = "dim_unit_ternak"
    
    id = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer)
    nama_unit = Column(String(255))
    alamat = Column(Text)
    longitude = Column(Float)
    latitiude = Column(Float)

class DimWaktu(Base, LoadDtMixin):
    __tablename__ = "dim_waktu"

    id = Column(Integer, primary_key=True)
    tahun = Column(Integer)
    bulan = Column(Integer)
    minggu = Column(Integer)
    tanggal = Column(Integer)

# Fact
class FactDistribusi(Base, LoadDtMixin):
    __tablename__ = "fact_distribusi"

    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer, primary_key=True)
    id_mitra_bisnis = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    jumlah_distribusi = Column(Integer)
    harga_minimum = Column(Integer)
    harga_maksimum = Column(Integer)
    harga_rata_rata = Column(Integer)
    jumlah_penjualan = Column(Integer)

class FactPopulasi(Base, LoadDtMixin):
    __tablename__ = "fact_populasi"

    id_peternakan = Column(Integer, primary_key=True)
    tanggal = Column(Integer, primary_key=True)
    jenis_kelamin = Column(Integer, primary_key=True)
    tipe_ternak = Column(Integer, primary_key=True)
    jumlah_lahir = Column(Integer)
    jumlah_mati = Column(Integer)
    jumlah_masuk = Column(Integer)
    jumlah_keluar = Column(Integer)
    jumlah = Column(Integer)

class FactProduksi(Base, LoadDtMixin):
    __tablename__ = "fact_produksi"

    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer, primary_key=True)
    id_sumber_pasokan = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    tanggal = Column(Date, primary_key=True)
    jumlah_produksi = Column(Integer)