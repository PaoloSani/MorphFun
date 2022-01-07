
import os
import warnings
import tensorflow as tf

warnings.filterwarnings("ignore")

    
    

def get_model_path(model_name):
    model_path = os.path.join(os.getcwd(), f'models/{model_name}')
    return model_path
    

def get_model_files_paths(model_dir) :
    #Getting the right ckpt file
    ckpt_files = [f for f in tf.io.gfile.listdir(model_dir) if 'ckpt' in f]
    ckpt_name = ckpt_files[0].split('.')[0]
    ckpt = os.path.join(model_dir, ckpt_name)
    
    #Getting the model files path
    model_data = {"dataset_stats_file": os.path.join(
        model_dir, 'dataset_statistics.pkl'),
        "gin_file": os.path.join(model_dir, 'operative_config-0.gin'),
        "ckpt": ckpt}
    
    return model_data



def get_useful_model_paths(model_names):
    model_useful_paths = {}
    for model_name in model_names:
        model_dir_path = get_model_path(model_name)
        model_useful_paths[f'{model_name}'] = {**get_model_files_paths(model_dir_path), **{"model_dir" : model_dir_path}}
        
    return model_useful_paths
    


    