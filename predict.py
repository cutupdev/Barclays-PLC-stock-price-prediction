import numpy as np
from tensorflow import keras
from datetime import datetime, timedelta
import csv
import value_scaler



def predict(target, past, future, std_path, data_path):

    open_price, close_price, high_price, low_price, volume = value_scaler.value_scale(data_path, std_path)

    # Load saved data
    with open(std_path, newline='') as csvfile:
        mean_std = csv.DictReader(csvfile)
        for row in mean_std:
            if target == 'close':
                convert_mean = float(row['close_mean'])
                convert_std = float(row['close_std'])
            elif target == 'high':
                convert_mean = float(row['high_mean'])
                convert_std = float(row['high_std'])
            elif target == 'low':
                convert_mean = float(row['low_mean'])
                convert_std = float(row['low_std'])
            else:
                convert_mean = float(row['open_mean'])
                convert_std = float(row['open_std'])
    
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
        if target == 'close':
            target_data[i] = close_price[i]
        elif target == 'high':
            target_data[i] = high_price[i]
        elif target == 'low':
            target_data[i] = low_price[i]
        else:
            target_data[i] = open_price[i]

    model = keras.models.load_model("models/" + target + ".keras") # Model load 

    predicts = np.zeros((future,)) # Prediction value

    # Prediction
    for x in range(future):
        if x < (future-1):
            predict_data = input_data[x-(past+future-1):x-(future-1)]
        else:
            predict_data = input_data[x-(past+future-1):]
        predict_data = predict_data.reshape((1, past, future))
        print(target, "========>", predict_data * convert_std + convert_mean)
        predict_value = model.predict(predict_data)
        real_predict = predict_value * convert_std + convert_mean
        predicts[x] = real_predict

    past_value = np.zeros((past,))
    past_value = open_price[-past:]
    past_value = past_value * convert_std + convert_mean

    return past_value, predicts



def getDate(data_path, past, future):

    dateframe = value_scaler.get_dateframe(data_path)

    # Convert date strings to datetime objects
    dates = [datetime.strptime(date_string, '%Y-%m-%d') for date_string in dateframe[-past:]]

    # Find the last date
    last_date = max(dates)

    # Generate future new dates, each a day after the last
    new_dates = [last_date + timedelta(days=i) for i in range(1, future+1)]

    # Combine the original dates with the new dates and convert back to strings
    combined_dates = dateframe[-past:] + [date.strftime('%Y-%m-%d') for date in new_dates]

    return combined_dates