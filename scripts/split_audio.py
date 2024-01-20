import warnings
import glob
import numpy as np
from pydub import AudioSegment

warnings.filterwarnings("ignore")
FILES_PATTERN = glob.glob("./audio/*.aac")
counter = 0


def load_audio(file_path):
    audio = AudioSegment.from_file(file_path, format="aac")
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    samples /= np.max(np.abs(samples), axis=0)
    
    return samples


def split_audio(audio_array):
    mean_threshold = 0.75
    gap = 100_000
    max_n_shots = 6
    i = 0
    peaks = []

    while i < len(audio_array) - 1:
        if len(peaks) > max_n_shots:
            break
        if np.mean([audio_array[i], audio_array[i+1]]) > mean_threshold:
            peaks.append(i)
            i += gap
        else:
            i += 2

    return peaks


def save_audio(file_path, peaks, j, output_folder='audio_splitted/'):
    audio = AudioSegment.from_file(file_path, format="aac")
    time_before = 40_000
    time_after = 60_000
    global counter

    for i, peak_index in enumerate(peaks):
        counter += 1
        start_index = peak_index - time_before  
        end_index = peak_index + time_after

        start_time = start_index // 95
        end_time = end_index // 95

        output_file = f"{output_folder}shot_{j+1}-{i+1}.wav"
        segment = audio[start_time:end_time]
        segment.export(output_file, format="wav")

        print(f"   {i+1}: start time: {start_time/1000} s, end time: {end_time/1000} s, nr {j+1}-{i+1}")


if __name__ == "__main__":
    for j, file in enumerate(FILES_PATTERN):
        audio_file = file
        print("\nFile name: ", audio_file)

        audio_array = load_audio(audio_file)
        peaks = split_audio(audio_array)
        save_audio(audio_file, peaks, j)

    print(f"\nTotal number of shots: {counter}")


    


