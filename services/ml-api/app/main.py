import os
import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import Optional
from typing_extensions import Annotated

import app.models as models

from app.database import engine, SessionLocal
from app.helpers import *
from app.models import *
from app.schemas import *

ENV_PATH = '.env'

models.Base.metadata.create_all(bind=engine)

load_dotenv(ENV_PATH)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

model_dict = load_model()
scaler_dict = load_scaler()


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'status': "error",
            'type': "REQUEST_VALIDATION_ERROR",
            'message': f"{exc.errors()[0]['loc'][1]}: {exc.errors()[0]['msg']}"
        }
    )

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={
            'status': "error",
            'type': "INTERNAL_SERVER_ERROR",
            'message': "something went wrong."        
        }
    )


@app.post(
    path="/predict", 
    name="run_milk_prediction",
    responses={
        status.HTTP_200_OK: {
            'model': PredictionSuccessResponse,
            'description': "Prediction success"
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': PredictionFailureResponse,
            'description': "There is bad request from client"
        },
        status.HTTP_404_NOT_FOUND: {
            'model': PredictionFailureResponse,
            'description': "Data not found"
        }
    }
)
async def create_prediction(
    predict_request: PredictionRequest, 
    db: Session = Depends(get_db)
):
    
    predict_input = PredictionObj(**predict_request.model_dump())
        
    # get id lokasi 
    if (predict_input.regency is None) or (predict_input.regency == ''):
        id_lokasi = (
            db.query(DimLokasi.id)
            .where(and_(DimLokasi.provinsi == predict_input.province,
                        DimLokasi.kabupaten_kota == None))
            .first()
        )

        # handle id_lokasi not found
        if id_lokasi is not None:
            id_lokasi = id_lokasi[0]
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "id_lokasi not found"
                }
            )
    
    else:
        id_lokasi = (
            db.query(DimLokasi.id)
            .where(and_(DimLokasi.provinsi == predict_input.province,
                        DimLokasi.kabupaten_kota == predict_input.regency))
            .first()
        )
        
        # handle id_lokasi not found
        if id_lokasi is not None:
            id_lokasi = id_lokasi[0]
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "id_lokasi not found"
                }
            )
    
    # get id unit ternak
    if predict_request.unit is not None:
        id_unit_ternak = (
            db.query(DimUnitTernak.id)
            .where(DimUnitTernak.nama_unit == predict_input.unit)
            .first()
        )
        
        if id_unit_ternak is not None:
            id_unit_ternak = id_unit_ternak[0]
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "id_unit_ternak not found"
                }
            )
    
    else:
        id_unit_ternak = None
        
    
    if predict_input.time_type == 'daily':
        
        date_list = create_date_range(start_date=predict_input.start_date, 
                                      end_date=predict_input.end_date)
        
        id_tanggal_list = []
        for dt in date_list:
            id_tanggal = (
                db.query(DimWaktu.id)
                .where(and_(DimWaktu.tahun == dt[0],
                            DimWaktu.bulan == dt[1],
                            DimWaktu.tanggal == dt[2]))
                .first()
            )
            
            # handle date not found in dwh
            if id_tanggal is None:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'status': "error",
                        'type': "DATA_NOT_FOUND",
                        'message': f"date ({dt[0]}-{dt[1]}-{dt[2]}) not found in database"
                    }
                )
            
            id_tanggal_list.append(id_tanggal[0])
        
        # get data input for prediction
        input_data_list = []
        for id_tanggal in id_tanggal_list:
            
            data = (
                db.query(FactProduksi.jumlah_produksi)
                .where(and_(FactProduksi.id_waktu == id_tanggal,
                            FactProduksi.id_lokasi == id_lokasi,
                            FactProduksi.id_unit_ternak == id_unit_ternak))
                .all()
            )
            
            if len(data) == 0:
                data_pred = (
                    db.query(PredSusu.prediction)
                    .where(and_(PredSusu.id_waktu == id_tanggal,
                                PredSusu.id_lokasi == id_lokasi,
                                PredSusu.id_unit_ternak == id_unit_ternak))
                    .first()
                    )
                
                if data_pred is None:
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            'status': "error",
                            'type': "DATA_NOT_FOUND",
                            'message': "there is missing data for input prediction."
                        }
                    )
                else:
                    input_data_list.append([id_tanggal, float(data_pred[0])])
            else:
                sum_data = 0
                for dt in data:
                    sum_data += dt[0]
                input_data_list.append([id_tanggal, sum_data])
        
        # format input data 
        input_data_df = pd.DataFrame(input_data_list, columns=['id_tanggal', 'data'])

        try:
            model = model_dict[predict_request.time_type][predict_input.folder_name]
        except:
            model = None
            
        try:
            scaler = scaler_dict[predict_request.time_type][predict_input.folder_name]
        except:
            scaler = None
        
        if (model is None) or (scaler is None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "model or scaler not found."
                }
            )
        
        input_data_df['dt'] = scaler.transform(input_data_df['data'].values.reshape(-1, 1))
        input_data_model = input_data_df['data'].values.tolist()
        
        input_data_model = np.array(input_data_model).reshape(1, int(os.getenv('LOOK_BACK')))
        input_data_model = np.reshape(input_data_model, (input_data_model.shape[0], 1, input_data_model.shape[1]))
        
        pred_data = model.predict(input_data_model)
        pred_data = scaler.inverse_transform(pred_data)[0][0].item()
        pred_data = round(pred_data, 2)
        
        # Check prediction result in database
        id_waktu = (
            db.query(DimWaktu.id)
            .where(and_(DimWaktu.tahun == predict_input.date.year,
                        DimWaktu.bulan == predict_input.date.month,
                        DimWaktu.tanggal == predict_input.date.day))
            .first()
        )
        
        if id_waktu is not None:
            id_waktu = id_waktu[0]
        else:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "id_waktu not found in dim_waktu table."
                }
            )
        
        pred_in_database = (
            db.query(PredSusu)
            .filter(and_(PredSusu.id_waktu == id_waktu,
                         PredSusu.id_lokasi == id_lokasi,
                         PredSusu.id_unit_ternak == id_unit_ternak))
            .first()
        )
        
        if pred_in_database is None:
            new_prediction = PredSusu(
                id_waktu=id_waktu,
                id_lokasi=id_lokasi,
                id_unit_ternak=id_unit_ternak,
                prediction=pred_data
            )
            
            db.add(new_prediction)
            db.commit()
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': "success",
                    'message': "add new prediction result."
                }
            )
            
        else:
            pred_in_database = float(pred_in_database.prediction)
            
            if (round(pred_data, 2) != round(pred_in_database, 2)):
                update_data = (
                    db.query(PredSusu)
                    .where(and_(PredSusu.id_waktu == id_waktu,
                                PredSusu.id_lokasi == id_lokasi,
                                PredSusu.id_unit_ternak == id_unit_ternak))
                    .first()
                )
                
                update_data.prediction = pred_data
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'status': "success",
                        'message': "update prediction in database."
                    }
                )
                
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': "success",
                    'message': "OK"
                }
            )
            
    else:
        # This is for weekly prediction
        pass
    
        return

       