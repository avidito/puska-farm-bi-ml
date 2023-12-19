import joblib
import os, sys
import tensorflow as tf

CWD_PATH = os.getcwd()

def load_model():
    
    model_path = os.path.join(CWD_PATH, os.getenv('MODEL_PATH'))
    
    
    model_dict = {}
    
    for time_type in os.listdir(model_path):
        
        if (time_type == '.DS_Store'):
            continue
        
        model_dict[time_type] = {}
        
        for folder in os.listdir(os.path.join(model_path, time_type)):
            
            if (folder == '.DS_Store'):
                continue
            
            try:
                model_dict[time_type][folder] = tf.keras.models.load_model(
                    os.path.join(model_path, time_type, folder, 'model.h5')
                )
            except:
                model_dict[time_type][folder] = None
                
    return model_dict
    
 
def load_scaler():
    
    scaler_path = os.path.join(CWD_PATH, os.getenv('SCALER_PATH'))
    
    scaler_dict = {}
    
    for time_type in os.listdir(scaler_path):
        
        if (time_type == '.DS_Store'):
            continue
        
        scaler_dict[time_type] = {}
        
        for folder in os.listdir(os.path.join(scaler_path, time_type)):
            
            if (folder == '.DS_Store'):
                continue
            
            try:
                scaler_dict[time_type][folder] = joblib.load(
                    os.path.join(scaler_path, time_type, folder, 'scaler.joblib')
                )
            except:
                scaler_dict[time_type][folder] = None
            
    return scaler_dict
    
  