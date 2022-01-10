import os
import pickle

class Util:

    @classmethod
    def dump(cls, value, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(value, f)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        return data

    @classmethod
    def data_cancat(cls, data_path, file_name):
    
        data_dirs = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
        data_list = []
        for data_dir in data_dirs:
            if os.path.isfile(os.path.join(data_path+data_dir, file_name)):
                df = load(os.path.join(data_path+data_dir, file_name))
                data_list.append(df)
        
        return pd.concat(data_list, axis=0)