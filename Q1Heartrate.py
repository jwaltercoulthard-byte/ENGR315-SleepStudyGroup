import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal as sig

"""
Collection of Methods for Heart Rate Analysis and graphing to be used in Q5
    
Includes methods for loading data, calculating heart rate statistics, and generating plots.
"""


def load_heart_data(usernum):
    """
    Load heart rate data for a specific user from a CSV file.

    Parameters:
    usernum (int): The user number to load data for.

    Returns:
    pd.DataFrame: A DataFrame containing the heart rate data with timestamps.
    sleep times as designated by sleep.csv
    """
    # get data from actigraph and sleep
    try:
        data = pd.read_csv(f"Data/DataPaper/user_{usernum}/Actigraph.csv")
        sleep_data = pd.read_csv(f"Data/DataPaper/user_{usernum}/sleep.csv")

    except FileNotFoundError:
        print(f"File not found.")
        return None

    # convert sleeptimes to numpy array for easier processing
    sleep_data = sleep_data.loc[
        :, ["In Bed Date", "In Bed Time", "Out Bed Date", "Out Bed Time"]
    ].to_numpy()

    return data, sleep_data


def slice_data(data, sleep_times):
    """
    Slice heart rate data into one DataFrame per sleep cycle.

    Parameters:
    data (pd.DataFrame): The heart rate data with timestamps.
    sleep_times: Rows of (start day, start time, end day, end time).

    Returns:
    list[pd.DataFrame]: One DataFrame per sleep cycle. Timestamp seconds are
        preserved, while filtering is minute-based.
    """
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')
    data_day = pd.to_numeric(data['day'])
    minute_of_day = data['time'].dt.hour * 60 + data['time'].dt.minute
    slices = []

    for start_day, start_time, end_day, end_time in sleep_times:
        start_time = pd.to_datetime(start_time, format='%H:%M')
        end_time = pd.to_datetime(end_time, format='%H:%M')
        start_minute = start_time.hour * 60 + start_time.minute
        end_minute = end_time.hour * 60 + end_time.minute

        after_start = (data_day > start_day) | (
            (data_day == start_day) & (minute_of_day >= start_minute)
        )
        before_end = (data_day < end_day) | (
            (data_day == end_day) & (minute_of_day <= end_minute)
        )
        slices.append(data.loc[after_start & before_end])

    return slices


def find_heart_spikes(data, threshold=100, window_size=5):
    """
    Find heart rate peaks using a moving-average-smoothed signal.

    Parameters:
    data (pd.DataFrame): The heart rate data with timestamps.
    threshold (int): Minimum smoothed heart rate in BPM for a peak.
    window_size (int): Odd number of readings in the moving-average window.

    Returns:
    pd.Index: Indices of the original heart rate readings identified as peaks.
    """
    if window_size < 1 or window_size % 2 == 0:
        raise ValueError("window_size must be a positive odd number")

    heart_rate = data["HR"].to_numpy(dtype=float)
    if window_size > len(heart_rate):
        raise ValueError("window_size cannot exceed the number of readings")

    smoothed_hr = np.convolve(
        heart_rate, np.ones(window_size) / window_size, mode="valid"
    )

    #this sig function does the heavy lifting. Tune prominence as rise needed and distance as lockout
    peak_positions, _ = sig.find_peaks(
        smoothed_hr, height=threshold, prominence=20, distance=30
    )
    peak_positions = peak_positions + window_size // 2

    return data.index.take(peak_positions)

def plot_heart_rate(data, spikes=None):
    """
    Plot heart rate data with optional spike markers.

    Parameters:
    data (pd.DataFrame): The heart rate data with timestamps.
    spikes (pd.Index, optional): Indices of heart rate spikes to mark on the plot.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['time'], data['HR'], label='Heart Rate', color='blue')
    
    if spikes is not None:
        plt.scatter(data.loc[spikes, 'time'], data.loc[spikes, 'HR'], color='red', label='Spikes', zorder=5)
    
    plt.title('Heart Rate Over Time')
    plt.xlabel('Time')
    plt.ylabel('Heart Rate (BPM)')
    plt.legend()
    plt.grid()
    plt.show()



if __name__ == "__main__":
    usernum = 1  # Example user number
    data, sleep_time = load_heart_data(usernum)
    # if data is not None:
    #     print(data.head())
    #     print("Sleep times:", sleep_time)

    sliced_data = slice_data(data, sleep_time)
    # for cycle, sleep_slice in enumerate(sliced_data, start=1):
    #     print(f"Sleep cycle {cycle}:")
    #     print(sleep_slice)
    spikes = find_heart_spikes(data, threshold=105, window_size=3)
    print("Heart rate spikes found at indices:", spikes.tolist())

    plot_heart_rate(data, spikes=spikes)