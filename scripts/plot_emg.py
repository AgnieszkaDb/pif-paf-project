import warnings
import glob 
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

warnings.filterwarnings("ignore")

FILES_PATTERN = glob.glob("./emg_rms/*.csv")
GRAPHS_DIR = "./graphs/emg_graphs_rms"
NUM_FILES = len(FILES_PATTERN)


def extract_hour(file):
    base_name = os.path.basename(file)
    name = os.path.splitext(base_name)[0]

    date_str = name[len("data_collection_"):len("data_collection_") + 8]
    time_str = name[len("data_collection_") + 8:]

    datetime_str = f"{date_str} {time_str}"
    formatted_datetime = datetime.strptime(datetime_str, "%Y%m%d %H%M%S") 

    return formatted_datetime.strftime("%H%M")


def plot_emg(file, i):
    df = pd.read_csv(file)
    if GRAPHS_DIR == "./emg_graphs":
        name = extract_hour(file)
    else:
        name = "rms"

    plt.figure(figsize=(15, 6))  

    plt.plot(df['Index'], df['V1'], label='G. długa mięśnia trójgłowego', linewidth=0.7)
    plt.plot(df['Index'], df['V2'], label='Zginacz promieniowy nadgarstka', linewidth=0.7)

    plt.xlabel('Indeks')
    plt.ylabel('Wartość')
    plt.title(str(name))
    plt.legend() 
    plt.grid() 
    plt.xticks(np.arange(min(df['Index']), max(df['Index']) + 1, 50))
     
    plt.savefig(os.path.join(GRAPHS_DIR, str(i+1) + "_emg_" + name))


if __name__ == "__main__":
    sorted_files = sorted(FILES_PATTERN)

    for i, file in tqdm(enumerate(sorted_files), total=NUM_FILES):
        plot_emg(file, i)
        # extract_hour(file)

