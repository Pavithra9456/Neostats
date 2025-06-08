import pandas as pd

def load_excel(uploaded_file):
    return pd.read_excel(uploaded_file)

def preprocess(df):
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('[^a-zA-Z0-9]', '', regex=True)
    return df