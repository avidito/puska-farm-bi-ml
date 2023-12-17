import os
import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import and_
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from starlette import status

import app.models as models

from app.database import engine, SessionLocal
from app.helpers import load_model, load_scaler
from app.models import ProduksiSusu, UnitTernak, Wilayah, PredictionSusuDailyProvince, PredictionSusuDailyRegency, PredictionSusuDailyUnit

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
    date: date
    time_type: str
    province: str
    regency: str
    unit: str

app = FastAPI()

@app.post("/predict", status_code=status.HTTP_200_OK)
async def create_prediction(predict_request: PredictionRequest, db: Session = Depends(get_db)):
    
    today_date = predict_request.date
    start_date = today_date - timedelta(int(os.getenv('LOOK_BACK')))
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = today_date - timedelta(1)
    end_date = end_date.strftime("%Y-%m-%d")
    
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
    