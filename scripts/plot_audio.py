import librosa
import librosa.display
import matplotlib.pyplot as plt
from tqdm import tqdm
import glob
import os
import warnings

warnings.filterwarnings("ignore")

FILES_PATTERN = glob.glob("./audio/*.aac")
GRAPHS_DIR = "./audio_graphs"
NUM_FILES = len(FILES_PATTERN)

  
def load_audio(file_path):
    samples, frame_rate = librosa.load(file_path, sr=None)
    return samples, frame_rate


def plot_waveform(samples, frame_rate, i):
    output_file = "_audio"
    if GRAPHS_DIR == "./audio_graphs" and i == 0:
        output_file = "_test_shots"

    plt.figure(figsize=(15, 5))

    librosa.display.waveshow(samples, sr=frame_rate)

    plt.title(f'Waveform of Audio Signal {i}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(GRAPHS_DIR, str(i) + output_file))
    plt.close()


if __name__ == "__main__":
    sorted_files = sorted(FILES_PATTERN)

    for i, file in tqdm(enumerate(sorted_files), total=NUM_FILES):
        samples, frame_rate = load_audio(file)
        plot_waveform(samples, frame_rate, i)
        

        
