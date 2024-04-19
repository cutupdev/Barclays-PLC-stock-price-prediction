import os
import numpy as np
import csv



def value_scale(data_path, std_path):

    open_price, close_price, high_price, low_price, volume = get_value(data_path) 

    # Load saved data
    with open(std_path, newline='') as csvfile:
        mean_std = csv.DictReader(csvfile)
        for row in mean_std:
            open_mean = float(row['open_mean'])
            open_std_mean = float(row['open_std'])
            close_mean = float(row['close_mean'])
            close_std_mean = float(row['close_std'])
            high_mean = float(row['high_mean'])
            high_std_mean = float(row['high_std'])
            low_mean = float(row['low_mean'])
            low_std_mean = float(row['low_std'])
            volume_mean = float(row['volume_mean'])
            volume_std_mean = float(row['volume_std'])
            print("this is value ==>", row['open_mean'], "<== this is value")

    # Open price standardization
    open_price -= open_mean
    open_price /= open_std_mean

    # Close price standardization
    close_price -= close_mean
    close_price /= close_std_mean

    # High price standardization
    high_price -= high_mean
    high_price /= high_std_mean

    # Low price standardization
    low_price -= low_mean
    low_price /= low_std_mean

    # Volume standardization
    volume -= volume_mean
    volume /= volume_std_mean

    return open_price, close_price, high_price, low_price, volume



def calculate_std(data_path, std_path):

    open_price, close_price, high_price, low_price, volume = get_value(data_path) 

    # Open price standardization   
    open_mean = open_price[:].mean(axis=0)
    open_price -= open_mean
    open_std_mean = open_price[:].std(axis=0)

    # High price standardization 
    high_mean = high_price[:].mean(axis=0)
    high_price -= high_mean
    high_std_mean = high_price[:].std(axis=0)

    # Low price standardization 
    low_mean = low_price[:].mean(axis=0)
    low_price -= low_mean
    low_std_mean = low_price[:].std(axis=0)

    # Close price standardization 
    close_mean = close_price[:].mean(axis=0)
    close_price -= close_mean
    close_std_mean = close_price[:].std(axis=0)

    # Volume standardization
    volume_mean = volume[:].mean(axis=0)
    volume -= volume_mean
    volume_std_mean = volume[:].std(axis=0)

    # Save calculated values in csv file
    headers = ["open_mean", "open_std", "close_mean", "close_std", "high_mean", "high_std", "low_mean", "low_std", "volume_mean", "volume_std"]
    data = [open_mean, open_std_mean, close_mean, close_std_mean, high_mean, high_std_mean, low_mean, low_std_mean, volume_mean, volume_std_mean]

    # Open/Create a new CSV file
    with open(std_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(headers)
        
        # Write the data
        writer.writerow(data)



def get_value(data_path):

    # File load
    fname = os.path.join(data_path)
    
    with open(fname) as f:
        data = f.read()
    
    lines = data.split("\n")
    lines = lines[0:-1]
    lines = lines[1:]

    # Series variables
    open_price = np.zeros((len(lines),))
    close_price = np.zeros((len(lines),))
    high_price = np.zeros((len(lines),))
    low_price = np.zeros((len(lines),))
    volume = np.zeros((len(lines),))

    # Train data extraction
    for i, line in enumerate(lines):
        values = [float(x) for x in line.split(",")[1:]]
        open_price[i] = values[0] 
        high_price[i] = values[1] 
        low_price[i] = values[2] 
        close_price[i] = values[3] 
        volume[i] = values[4]
    
    return open_price, close_price, high_price, low_price, volume



def get_dateframe(data_path):

    # File load
    fname = os.path.join(data_path)
    
    with open(fname) as f:
        data = f.read()
    
    lines = data.split("\n")
    lines = lines[0:-1]
    lines = lines[1:]

    dateframe = []

    for i, line in enumerate(lines):
        dateframe.append(line.split(",")[0])



calculate_std('datasets/barc.csv', 'datasets/financial_data.csv')