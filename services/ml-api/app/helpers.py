import joblib
import os, sys
import tensorflow as tf

CWD_PATH = os.getcwd()

def load_model():
    
    model_path = os.path.join(CWD_PATH, os.getenv('MODEL_PATH'))
    
    
    model_dict = {}
    
    for time_type in os.listdir(model_path):
        model_dict[time_type] = {}
        
        for folder in os.listdir(os.path.join(model_path, time_type)):
            if not ('-' in folder):
                try:
                    model_dict[time_type][model_dict] = 10
                except:
                    pass
            
                
    return model_dict
    
    
    
    for time_type in os.listdir(model_path):
        model_dict[time_type] = {}
        
        for province in os.listdir(os.path.join(model_path, time_type)):
            model_dict[time_type][province] = {}
            
            for regency in os.listdir(os.path.join(model_path, time_type, province)):
                if regency == 'model.h5':
                    try:
                        model_dict[time_type][province]['model'] = tf.keras.models.load_model(
                            os.path.join(model_path, time_type, province, 'model.h5')
                        )
                    except:
                        model_dict[time_type][province]['model'] = None
                    continue
                
                model_dict[time_type][province][regency] = {}
                
                for unit in os.listdir(os.path.join(model_path, time_type, province, regency)):
                    if unit == 'model.h5':
                        try:
                            model_dict[time_type][province][regency]['model'] = tf.keras.models.load_model(
                                os.path.join(model_path, time_type, province, regency, 'model.h5')
                            )
                        except:
                            model_dict[time_type][province][regency]['model'] = None
                        continue
                    
                    model_dict[time_type][province][regency][unit] = {}
                    try:
                        model_dict[time_type][province][regency][unit]['model'] = tf.keras.models.load_model(
                            os.path.join(model_path, time_type, province, regency, unit, 'model.h5')
                        )
                    except:
                        model_dict[time_type][province][regency][unit]['model'] = None
                
                if not 'model' in model_dict[time_type][province][regency]:
                    model_dict[time_type][province][regency]['model'] = None
            
            if not 'model' in model_dict[time_type][province]:
                model_dict[time_type][province]['model'] = None

    return model_dict   

def load_scaler():
    
    scaler_path = os.path.join(CWD_PATH, os.getenv('SCALER_PATH'))
    
    scaler_dict = {}
    
    for time_type in os.listdir(scaler_path):
        scaler_dict[time_type] = {}
        
        for province in os.listdir(os.path.join(scaler_path, time_type)):
            scaler_dict[time_type][province] = {}
            
            for regency in os.listdir(os.path.join(scaler_path, time_type, province)):
                if regency == 'scaler.joblib':
                    try:
                        scaler_dict[time_type][province]['scaler'] = joblib.load(
                            os.path.join(scaler_path, time_type, province, 'scaler.joblib')
                        )
                    except:
                        scaler_dict[time_type][province]['scaler'] = None
                    continue
                
                scaler_dict[time_type][province][regency] = {}
                
                for unit in os.listdir(os.path.join(scaler_path, time_type, province, regency)):
                    if unit == 'scaler.joblib':
                        try:
                            scaler_dict[time_type][province][regency]['scaler'] = joblib.load(
                                os.path.join(scaler_path, time_type, province, regency, 'scaler.joblib')
                            )
                        except:
                            scaler_dict[time_type][province][regency]['scaler'] = None
                        continue
                    
                    scaler_dict[time_type][province][regency][unit] = {}
                    try:
                        scaler_dict[time_type][province][regency][unit]['scaler'] = joblib.load(
                            os.path.join(scaler_path, time_type, province, regency, unit, 'scaler.joblib')
                        )
                    except:
                        scaler_dict[time_type][province][regency][unit]['scaler'] = None
                
                if not 'scaler' in scaler_dict[time_type][province][regency]:
                    scaler_dict[time_type][province][regency]['scaler'] = None
            
            if not 'scaler' in scaler_dict[time_type][province]:
                scaler_dict[time_type][province]['scaler'] = None

    return scaler_dict