import warnings
import glob 
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

warnings.filterwarnings("ignore")

FILES_PATTERN = glob.glob("./emg_splitted/emg*.csv")
GRAPHS_DIR = "./emg_rms"
NUM_FILES = len(FILES_PATTERN)
WINDOW_SIZE = 2  


def rms(muscle):
    rms_values = []
    for i in range(len(muscle) - WINDOW_SIZE + 1):
        window = muscle[i:i + WINDOW_SIZE]
        rms = np.sqrt(np.mean(window**2))
        rms_values.append(int(rms))
    return rms_values


def load_save(file, i):
    df = pd.read_csv(file)
    triceps = df['V1']
    flexor = df['V2']

    rms_tri = rms(triceps)
    rms_flex = rms(flexor)

    df['V1'][WINDOW_SIZE - 1:] = rms_tri  
    df['V2'][WINDOW_SIZE - 1:] = rms_flex  

    output_file = os.path.join(GRAPHS_DIR, f"emg_rms_{i+1}.csv")
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    for i, file in tqdm(enumerate(FILES_PATTERN), total=NUM_FILES):
        load_save(file, i)


