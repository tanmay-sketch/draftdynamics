import pandas as pd
import numpy as np

def preprocess_data(file_path, post_2013=False):
    """Load and preprocess the draft trade data."""
    df = pd.read_csv(file_path)
    
    if post_2013:
        df = df[df['year'] >= 2013]
    
    def process_pick_columns(row, cols):
        picks = []
        for col in cols:
            if pd.notna(row[col]):
                pick_num = float(str(row[col]).split('-')[-1])
                picks.append(pick_num)
        return picks if picks else [np.nan]
    
    up_picks = df.apply(lambda row: process_pick_columns(row, df.columns[2:5]), axis=1)
    down_picks = df.apply(lambda row: process_pick_columns(row, df.columns[7:10]), axis=1)
    
    return up_picks, down_picks