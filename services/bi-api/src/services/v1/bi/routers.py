import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.shared.database import get_db, run_query
QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")

router = APIRouter(
    prefix = "/v1/bi",
    tags = ["v1", "productions"]
)


@router.get("/summary-jenis-produk")
def route_summary_jenis_produk(db: Session = Depends(get_db)):
    params = {}
    data = run_query(db, QUERY_DIR, "summary_jenis_produk", params)
    return data

@router.get("/history-by-jenis-produk/{id_jenis_produk}")
def route_history_by_jenis_produk(id_jenis_produk: int, db: Session = Depends(get_db)):
    params = {
        "id_jenis_produk": id_jenis_produk
    }
    data = run_query(db, QUERY_DIR, "history_by_jenis_produk", params)
    return data

@router.get("/summary-populasi")
def route_summary_populasi(db: Session = Depends(get_db)):
    params = {}
    data = run_query(db, QUERY_DIR, "summary_populasi", params)
    return data

@router.get("/summary-populasi-by-provinsi")
def route_summary_populasi_by_provinsi(db: Session = Depends(get_db)):
    params = {}
    data = run_query(db, QUERY_DIR, "summary_populasi_by_provinsi", params)
    return data

@router.get("/summary-populasi-by-unit-ternak")
def route_summary_populasi_by_unit_ternak(db: Session = Depends(get_db)):
    params = {}
    data = run_query(db, QUERY_DIR, "summary_populasi_by_unit_ternak", params)
    return data