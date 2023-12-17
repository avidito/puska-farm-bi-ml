from sqlalchemy import Column, BigInteger, Numeric, String, Date, DateTime, Text, Float

from app.database import Base

class ProduksiSusu(Base):
    __tablename__ = 'produksi_susu'

    id = Column(BigInteger, primary_key=True)
    tgl_produksi = Column(Date)
    jumlah = Column(Numeric)
    satuan = Column(String)
    sumber_pasokan = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created_by = Column(BigInteger)
    updated_by = Column(BigInteger)
    deleted_by = Column(BigInteger)
    id_unit_ternak = Column(BigInteger)
    id_jenis_produk = Column(BigInteger)
    
class UnitTernak(Base):
    __tablename__ = 'unit_ternak'

    id = Column(BigInteger, primary_key=True)
    nama_unit = Column(String)
    alamat = Column(Text)
    provinsi_id = Column(BigInteger)
    kota_id = Column(BigInteger)
    kecamatan_id = Column(BigInteger)
    kelurahan_id = Column(BigInteger)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created_by = Column(BigInteger)
    updated_by = Column(BigInteger)
    deleted_by = Column(BigInteger)

class Wilayah(Base):
    __tablename__ = 'wilayah'

    id = Column(BigInteger, primary_key=True)
    kode = Column(String)
    nama = Column(String)
    
class PredictionSusuDailyProvince(Base):
    __tablename__ = 'prediction_susu_daily_province'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date)
    province = Column(String)
    prediction = Column(Float)
    
class PredictionSusuDailyRegency(Base):
    __tablename__ = 'prediction_susu_daily_regency'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date)
    regency = Column(String)
    prediction = Column(Float)
    
class PredictionSusuDailyUnit(Base):
    __tablename__ = 'prediction_susu_daily_unit'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date)
    unit = Column(String)
    prediction = Column(Float)