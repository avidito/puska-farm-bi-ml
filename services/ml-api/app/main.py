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
            .filter(and_(DimLokasi.provinsi == predict_request.province,
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
            .filter(and_(DimLokasi.provinsi == predict_request.province,
                         DimLokasi.kabupaten_kota  == predict_request.regency))
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
                .first()
            )
            
            if (data is None):
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
                input_data_list.append([id_tanggal, data[0]])
        
        # format input data 
        input_data_df = pd.DataFrame(input_data_list, columns=['id_tanggal', 'data'])
        
        return
    else:
        # This is for weekly prediction
        pass
    
    return
    if predict_request.time_type == '':
        raise HTTPException(status_code=404, detail='Time type should be not empty')
    
    if predict_request.province == '':
        raise HTTPException(status_code=404, detail='Province should be not empty')
    else:
        if predict_request.regency == '':

            data = (
                db.query(ProduksiSusu.tgl_produksi, ProduksiSusu.jumlah)
                .join(UnitTernak, ProduksiSusu.id_unit_ternak == UnitTernak.id)
                .join(Wilayah, UnitTernak.provinsi_id == Wilayah.id)
                .filter(and_(Wilayah.nama == predict_request.province, 
                             ProduksiSusu.tgl_produksi.between(start_date, end_date)))
                .all()
            )
            
            data = pd.DataFrame(data, columns=['tgl_produksi', 'jumlah'])
            
            model = model_dict[predict_request.time_type][predict_request.province]['model']
            scaler = scaler_dict[predict_request.time_type][predict_request.province]['scaler']
            
            predict_type = 'province'
            
        else:
            if predict_request.unit == '':
                
                data = (
                    db.query(ProduksiSusu.tgl_produksi, ProduksiSusu.jumlah)
                    .join(UnitTernak, ProduksiSusu.id_unit_ternak == UnitTernak.id)
                    .join(Wilayah, UnitTernak.kota_id == Wilayah.id)
                    .filter(and_(Wilayah.nama == predict_request.regency, 
                                 ProduksiSusu.tgl_produksi.between(start_date, end_date)))
                    .all()
                )
                
                data = pd.DataFrame(data, columns=['tgl_produksi', 'jumlah'])
                
                model = model_dict[predict_request.time_type][predict_request.province][predict_request.regency]['model']
                scaler = scaler_dict[predict_request.time_type][predict_request.province][predict_request.regency]['scaler']
                
                predict_type = 'regency'
                
            else:
                
                data = (
                    db.query(ProduksiSusu.tgl_produksi, ProduksiSusu.jumlah)
                    .join(UnitTernak, ProduksiSusu.id_unit_ternak == UnitTernak.id)
                    .filter(and_(UnitTernak.nama_unit == predict_request.unit, 
                                 ProduksiSusu.tgl_produksi.between(start_date, end_date)))
                    .all()
                )
                
                data = pd.DataFrame(data, columns=['tgl_produksi', 'jumlah'])
                
                model = model_dict[predict_request.time_type][predict_request.province][predict_request.regency][predict_request.unit]['model']
                scaler = scaler_dict[predict_request.time_type][predict_request.province][predict_request.regency][predict_request.unit]['scaler']
                
                predict_type = 'unit'
                
    if len(data) == 0:
        raise HTTPException(status_code=404, detail='Data history not found')
    
    if model == None:
        raise HTTPException(status_code=404, detail='Model not found')
    
    if scaler == None:
        raise HTTPException(status_code=404, detail='Scaler  not found')
    
    if predict_request.time_type == 'daily':
        data['tgl_produksi'] = pd.to_datetime(data['tgl_produksi'])
        
        agg_data = data.groupby('tgl_produksi')['jumlah'].mean().reset_index()  
        agg_data['jumlah'] = agg_data['jumlah'].astype(float).round(2)
        
        expected_date_range = pd.date_range(start=start_date, end=end_date)
        
        missing_dates = expected_date_range.difference(agg_data['tgl_produksi'])
      
        if len(missing_dates) > 0:
            
            for missing_date in missing_dates:
                
                if predict_type == 'province':
                    history_pred = (
                        db.query(PredictionSusuDailyProvince.prediction)
                        .filter(and_(PredictionSusuDailyProvince.province == predict_request.province),
                                     PredictionSusuDailyProvince.date == missing_date.date().strftime("%Y-%m-%d"))
                        .all()
                    )
                elif predict_type == 'regency':
                    history_pred = (
                        db.query(PredictionSusuDailyRegency.prediction)
                        .filter(and_(PredictionSusuDailyRegency.regency == predict_request.regency),
                                     PredictionSusuDailyRegency.date == missing_date.date().strftime("%Y-%m-%d"))
                        .all()
                    )
                elif predict_type == 'unit':
                    history_pred = (
                        db.query(PredictionSusuDailyUnit.prediction)
                        .filter(and_(PredictionSusuDailyUnit.unit == predict_request.unit),
                                     PredictionSusuDailyUnit.date == missing_date.date().strftime("%Y-%m-%d"))
                        .all()
                    )
                
                agg_data.loc[len(agg_data)] = [missing_date, history_pred[0][0]]
            
            agg_data = agg_data.sort_values(by='tgl_produksi')
            
        ## PREDICTION HERE
        jumlah_data = agg_data['jumlah']
        jumlah_data_2d = jumlah_data.values.reshape(-1, 1)
        agg_data['jumlah'] = scaler.transform(jumlah_data_2d)
        
        input_data = agg_data['jumlah'].values.tolist()
        input_data = np.array(input_data).reshape(1, int(os.getenv('LOOK_BACK')))
        input_data = np.reshape(input_data, (input_data.shape[0], 1, input_data.shape[1]))
        
        new_pred = model.predict(input_data)
        new_pred = scaler.inverse_transform(new_pred)[0][0].item()
        new_pred = round(new_pred, 2)
        
        if predict_type == 'province':
            old_pred = (
                db.query(PredictionSusuDailyProvince.prediction)
                .filter(and_(PredictionSusuDailyProvince.province == predict_request.province),
                             PredictionSusuDailyProvince.date == predict_request.date)
                .all()
            )
            
            if len(old_pred) > 0:
                if new_pred != old_pred[0][0]:
                    update_data = (
                        db.query(PredictionSusuDailyProvince)
                        .filter(PredictionSusuDailyProvince.province == predict_request.province,
                                PredictionSusuDailyProvince.date == predict_request.date)
                        .first()
                    )
                    
                    update_data.prediction = new_pred
            else:
                new_prediction = PredictionSusuDailyProvince(
                    date=predict_request.date,
                    province=predict_request.province,
                    prediction=new_pred
                )
                
                db.add(new_prediction)
            
            db.commit()
            
        elif predict_type == 'regency':
            old_pred = (
                db.query(PredictionSusuDailyRegency.prediction)
                .filter(and_(PredictionSusuDailyRegency.regency == predict_request.regency),
                             PredictionSusuDailyRegency.date == predict_request.date)
                .all()
            )
            
            if len(old_pred) > 0:
                if new_pred != old_pred[0][0]:
                    update_data = (
                        db.query(PredictionSusuDailyRegency)
                        .filter(PredictionSusuDailyRegency.regency == predict_request.regency,
                                PredictionSusuDailyRegency.date == predict_request.date)
                        .first()
                    )
                    
                    update_data.prediction = new_pred
            else:
                new_prediction = PredictionSusuDailyRegency(
                    date=predict_request.date,
                    regency=predict_request.regency,
                    prediction=new_pred
                )
                
                db.add(new_prediction)
            
            db.commit()
            
        elif predict_type == 'unit':
            old_pred = (
                db.query(PredictionSusuDailyUnit.prediction)
                .filter(and_(PredictionSusuDailyUnit.unit == predict_request.unit),
                             PredictionSusuDailyUnit.date == predict_request.date)
                .all()
            )
        
            if len(old_pred) > 0:
                if new_pred != old_pred[0][0]:
                    update_data = (
                        db.query(PredictionSusuDailyUnit)
                        .filter(PredictionSusuDailyUnit.unit == predict_request.unit,
                                PredictionSusuDailyUnit.date == predict_request.date)
                        .first()
                    )
                    
                    update_data.prediction = new_pred
            else:
                new_prediction = PredictionSusuDailyUnit(
                    date=predict_request.date,
                    unit=predict_request.unit,
                    prediction=new_pred
                )
                
                db.add(new_prediction)
            
            db.commit()
        
        return {'OK'}
        
    elif predict_request.time_type == 'weekly':
        pass
    