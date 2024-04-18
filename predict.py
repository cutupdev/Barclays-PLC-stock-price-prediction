import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from datetime import datetime, timedelta
import csv


def predict():
    # File load
    fname = os.path.join("barc.csv")
    
    with open(fname) as f:
        data = f.read()
    
    lines = data.split("\n")
    lines = lines[0:-1]
    header = lines[0].split(",")
    lines = lines[1:]

    # Series variables
    open_price = np.zeros((len(lines),))
    draw = np.zeros((len(lines),))
    high_price = np.zeros((len(lines),))
    low_price = np.zeros((len(lines),))
    close_price = np.zeros((len(lines),))
    volume = np.zeros((len(lines),))
    raw_data = np.zeros((len(lines), len(header) - 1))
    dateframe = []

    # Input data extraction
    for i, line in enumerate(lines):
        dateframe.append(line.split(",")[0])
        values = [float(x) for x in line.split(",")[1:]]
        open_price[i] = values[0] 
        draw[i] = values[0] 
        high_price[i] = values[1] 
        low_price[i] = values[2] 
        close_price[i] = values[3] 
        volume[i] = values[4]                       
        raw_data[i, :] = values[:] 

    # Load saved data
    with open("financial_data.csv", newline='') as csvfile:
        mean_std = csv.DictReader(csvfile)
        for row in mean_std:
            open_mean = float(row['open_mean'])
            open_std_mean = float(row['open_std'])
            high_mean = float(row['high_mean'])
            high_std_mean = float(row['high_std'])
            low_mean = float(row['low_mean'])
            low_std_mean = float(row['low_std'])
            close_mean = float(row['close_mean'])
            close_std_mean = float(row['close_std'])
            volume_mean = float(row['volume_mean'])
            volume_std_mean = float(row['volume_std'])
            print("this is value ==>", row['open_mean'], "<== this is value")

    # Open price standardization
    open_price -= open_mean
    open_price /= open_std_mean

    # High price standardization
    high_price -= high_mean
    high_price /= high_std_mean

    # Low price standardization
    low_price -= low_mean
    low_price /= low_std_mean

    # Close price standardization
    close_price -= close_mean
    close_price /= close_std_mean

    # Volume standardization
    volume -= volume_mean
    volume /= volume_std_mean

    length = len(high_price[:]) # Total data length
    input_data = np.zeros((length, 5)) # Input data
    target_data = np.zeros(length) # Target data

    # Input data generation
    for i, array in enumerate(input_data):
        input_data[i, 0] = open_price[i]
        input_data[i, 1] = high_price[i] 
        input_data[i, 2] = low_price[i] 
        input_data[i, 3] = close_price[i]
        input_data[i, 4] = volume[i]
        target_data[i] = open_price[i]

    model = keras.models.load_model("jena_dense.keras") # Model load 

    sequence_length = 10
    delay = 5
    predicts = np.zeros((delay,)) # Prediction value

    # Prediction
    for x in range(delay):
        if x < (delay-1):
            predict_data = input_data[x-(sequence_length+delay-1):x-(delay-1)]
        else:
            predict_data = input_data[x-(sequence_length+delay-1):]
        predict_data = predict_data.reshape((1, 10, 5))
        print(predict_data * open_std_mean + open_mean)
        predict_value = model.predict(predict_data)
        real_predict = predict_value * open_std_mean + open_mean
        predicts[x] = real_predict

    past_value = np.zeros((sequence_length,))
    past_value = open_price[-sequence_length:]
    past_value = past_value * open_std_mean + open_mean

    dates = getDate(dateframe[-10:])

    return past_value, predicts, dates


def getDate(origin):

    # Convert date strings to datetime objects
    dates = [datetime.strptime(date_string, '%Y-%m-%d') for date_string in origin]

    # Find the last date
    last_date = max(dates)

    # Generate 5 new dates, each a day after the last
    new_dates = [last_date + timedelta(days=i) for i in range(1, 6)]

    # Combine the original dates with the new dates and convert back to strings
    combined_dates = origin + [date.strftime('%Y-%m-%d') for date in new_dates]

    return combined_dates