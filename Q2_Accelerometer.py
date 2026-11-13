import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal as sig

"""
Collection of Methods for Accelerometer Analysis and graphing to be used in Q2
    
Includes methods for loading data, calculating accelerometer statistics, and generating plots.
"""
def load_accelerometer_data(usernum):
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
        :, ["In Bed Time", "Out Bed Time"]
    ]

    return data, sleep_data


def Parsed_data(data,sleep_times):
    new_data = pd.DataFrame()
    for row in range (0,len(sleep_times)):
        inbedtime, outbedtime = sleep_times.loc[row]
        temp_data = data[data["time"].between(inbedtime,outbedtime)]
        new_data = pd.concat([new_data,temp_data],ignore_index=True)
    print(f"Selected {len(new_data)} accelerometer readings.")
    
    return new_data


def calculate_accelerometer_magnitude(data):
    """
    Calculate basic statistics for accelerometer data.

    Parameters:
    data (pd.DataFrame): The accelerometer data DataFrame.

    Returns:
    np.ndarray: The calculated accelerometer magnitude array.
    """
    if data is None:
        return None

    X = data['Axis1'].to_numpy(dtype=float)
    Y = data['Axis2'].to_numpy(dtype=float)
    Z = data['Axis3'].to_numpy(dtype=float)
    
    Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
 
    return Magnitude


def plot_accelerometer_data(data,magnitude):
    """
    Plot the accelerometer magnitude data.

    Parameters:
    magnitude (np.ndarray): The accelerometer magnitude data array.
    """
    if data is None or magnitude is None or data.empty:
        return
    
    day = pd.to_numeric(data["day"])
    seconds_since_midnight = pd.to_timedelta(data["time"]).dt.total_seconds()
    elapsed_hours = (day - day.iloc[0]) * 24 + seconds_since_midnight / 3600
    elapsed_hours = elapsed_hours - elapsed_hours.iloc[0]

    plt.figure(figsize=(12, 6))
    plt.xlabel("Elapsed time (hours)")
    plt.ylabel("Magnitude")
    plt.title("Accelerometer Magnitude over time")
    plt.plot(elapsed_hours, magnitude, label='Magnitude', color='blue')
    plt.show()


if __name__ == "__main__":
    usernum = 1  # Example user number
    data, sleep_times = load_accelerometer_data(usernum)
    parsed_data = Parsed_data(data,sleep_times)
    magnitude = calculate_accelerometer_magnitude(parsed_data)
    plot_accelerometer_data(parsed_data,magnitude)
