import os
import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated

import app.models as models

from app.database import engine, SessionLocal
from app.helpers import *
from app.models import *

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

class PredictionRequest(BaseModel):
    date: Optional[date]
    time_type: str = None
    province: Optional[str] = None 
    regency: Optional[str] = None
    unit: Optional[str] = None
    
class PredictionResponse(BaseModel):
    message: str

app = FastAPI()

@app.post(
    path="/predict", 
    name="run_milk_prediction",
    responses={
        201: {
            'model': PredictionResponse,
            'description': "Prediction success"
        },
        400: {
            'model': PredictionResponse,
            'description': "There is bad request from client"
        },
        404: {
            'model': PredictionResponse,
            'description': "Data history not found"
        },
        422: {
            'model': PredictionResponse,
            'description': "Model or Scaler not found"
        }
    }
)
async def create_prediction(
    predict_request: PredictionRequest, 
    db: Session = Depends(get_db)
):
    
    # validate date field is required
    if (predict_request.date is None):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'message': 'date field is required.'
            }
        )
        
    # validate time type is required
    if (    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'message': 'time_type field is required.'
            }
        )
    
    # handle there is no filter input
    if ((predict_request.province is None) and 
        (predict_request.regency is None) and
        (predict_request.unit is None)) or \
       ((predict_request.province == '') and 
        (predict_request.regency == '') and
        (predict_request.unit == '')):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'message': "please fill province, regency, or unit field."
            }
        )
        
    # get id lokasi 
    if ((predict_request.regency is None) or (predict_request.regency == '')):
        id_lokasi = (
            db.query(DimLokasi.id)
            .filter(and_(DimLokasi.provinsi == predict_request.province.lower(),
                         DimLokasi.kabupaten_kota  == None))
            .first()
        )
        
        # handle id lokasi not found
        if (id_lokasi is None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'message': "id_lokasi not found"
                }
            )
        else:
            id_lokasi = id_lokasi[0]
            load_key = f"{predict_request.province.lower()}"
    
    else:
        id_lokasi = (
            db.query(DimLokasi.id)
            .filter(and_(DimLokasi.provinsi == predict_request.province.lower(),
                         DimLokasi.kabupaten_kota  == predict_request.regency.lower()))
            .first()
        )
        
        # handle id lokasi not found
        if (id_lokasi is None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'message': "id_lokasi not found"
                }
            )
        else:
            id_lokasi = id_lokasi[0]
            load_key = f"{predict_request.province.lower()}-{predict_request.regency.lower()}"
    
    # get id unit ternak
    if not (predict_request.unit is None):
        id_unit_ternak = (
            db.query(DimUnitTernak.id)
            .filter_by(nama_unit=predict_request.unit.lower())
            .first()
        )
        
        if (id_unit_ternak is None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'message': "id_unit_ternak not found"
                }
            )
        else:
            id_unit_ternak = id_unit_ternak[0]
            load_key = f"{predict_request.province.lower()}-{predict_request.regency.lower()}-{predict_request.unit.lower()}"
            
    else:
        id_unit_ternak = None
        
    
    if (predict_request.time_type.lower() == 'daily'):
        
        # get id waktu from dwh
        today_date = predict_request.date
        start_date = today_date - timedelta(int(os.getenv('LOOK_BACK')))
        end_date = today_date - timedelta(1)
        
        date_list = create_date_range(start_date, end_date)
        
        id_tanggal_list = []
        for dt in date_list:
            id_tanggal = (
                db.query(DimWaktu.id)
                .filter_by(tahun=dt[0],
                        bulan=dt[1],
                        tanggal=dt[2])
                .first()
            )
            
            # handle date not found in dwh
            if (id_tanggal is None):
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'message': f"date ({dt[0]}-{dt[1]}-{dt[2]}) not found in database"
                    }
                )
            
            id_tanggal_list.append(id_tanggal[0])
        
        # get data input for prediction
        input_data_list = []
        for id_tanggal in id_tanggal_list:
            
            data = (
                db.query(FactProduksi.jumlah_produksi)
                .filter(and_(FactProduksi.id_waktu == id_tanggal,
                             FactProduksi.id_lokasi == id_lokasi,
                             FactProduksi.id_unit_ternak == id_unit_ternak))
                .all()
            )
            
            if (len(data) == 0):
                data_pred = (
                    db.query(PredSusu.prediction)
                    .filter(and_(PredSusu.id_waktu == id_tanggal,
                                 PredSusu.id_lokasi == id_lokasi,
                                 PredSusu.id_unit_ternak == id_unit_ternak))
                    .first()
                    )
                
                if (data_pred is None):
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={
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
            model = model_dict[predict_request.time_type][load_key]
        except:
            model = None
            
        try:
            scaler = scaler_dict[predict_request.time_type][load_key]
        except:
            scaler = None
            
        if ((model is None) or (scaler is None)):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
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
            .filter(and_(DimWaktu.tahun == predict_request.date.year,
                         DimWaktu.bulan == predict_request.date.month,
                         DimWaktu.tanggal == predict_request.date.day))
            .first()
        )
        
        if (id_waktu is None):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    'message': "id_waktu not found in dim_waktu table."
                }
            )
        else:
            id_waktu = id_waktu[0]
            
        
        pred_in_database = (
            db.query(PredSusu)
            .filter(and_(PredSusu.id_waktu == id_waktu,
                         PredSusu.id_lokasi == id_lokasi,
                         PredSusu.id_unit_ternak == id_unit_ternak))
            .first()
        )
        
        if (pred_in_database is None):
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
                    'message': "add new prediction result."
                }
            )
            
        else:
            pred_in_database = float(pred_in_database.prediction)
            
            if (round(pred_data, 2) != round(pred_in_database, 2)):
                update_data = (
                    db.query(PredSusu)
                    .filter(and_(PredSusu.id_waktu == id_waktu,
                                 PredSusu.id_lokasi == id_lokasi,
                                 PredSusu.id_unit_ternak == id_unit_ternak))
                    .first()
                )
                
                update_data.prediction = pred_data
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'message': "update prediction in database."
                    }
                )
                
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'message': "OK"
                }
            )
            
    else:
        # This is for weekly prediction
        pass
    
        return

       