# data_loader.py
from imports import *

def load_data(file):
    if not os.path.exists(file):
        print(f"File {file} not found.")
        return pd.DataFrame()  # Return an empty DataFrame or handle as needed
    data = pd.read_csv(file, encoding='utf-8', lineterminator='\n')
    if 'created_at' in data.columns:
        data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')
    return data

