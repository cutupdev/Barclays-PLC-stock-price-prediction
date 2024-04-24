import numpy as np
from tensorflow import keras
import value_scaler
from glo_variable import TARGET_OPEN, TARGET_HIGH, TARGET_CLOSE, TARGET_LOW



def generate(past, future, target, data_path, std_path):

    open_price, high_price, low_price, close_price, volume = value_scaler.value_scale(data_path, std_path)

    length = len(open_price[:])
    train_data = np.zeros((length, 5))
    target_data = np.zeros(length)

    # Train data generation
    for i, data in enumerate(train_data):
        train_data[i, 0] = open_price[i]
        train_data[i, 1] = high_price[i] 
        train_data[i, 2] = low_price[i] 
        train_data[i, 3] = close_price[i] 
        train_data[i, 4] = volume[i]
        if target == TARGET_CLOSE:
            target_data[i] = close_price[i]
        elif target == TARGET_HIGH:
            target_data[i] = high_price[i]
        elif target == TARGET_LOW:
            target_data[i] = low_price[i]
        elif target == TARGET_OPEN:
            target_data[i] = open_price[i]
        else: 
            pass

    # Dataset generation parameters
    sampling_rate = 1
    sequence_length = past
    delay = sequence_length + future - 1
    batch_size = 8

    # Datasets length 
    num_train_samples = int(0.9 * len(train_data))
    num_val_samples = int(0.8 * len(train_data))
    num_test_samples = int(0.9 * len(train_data) - delay - 1)

    # Train datasets generation
    train_dataset = keras.utils.timeseries_dataset_from_array(
        data = train_data[:-future], 
        targets=target_data[delay:], 
        sampling_rate=sampling_rate,
        sequence_length=sequence_length, 
        shuffle=True,
        batch_size=batch_size,
        start_index=0)

    # Validation datasets generation
    val_dataset = keras.utils.timeseries_dataset_from_array(
        data = train_data[:-future],
        targets=target_data[delay:],
        sampling_rate=sampling_rate,
        sequence_length=sequence_length,
        shuffle=True,
        batch_size=batch_size,
        start_index=num_val_samples,
        end_index=num_test_samples)

    # Test datasets generation
    test_dataset = keras.utils.timeseries_dataset_from_array(
        data = train_data[:-future],
        targets=target_data[delay:],
        sampling_rate=sampling_rate,
        sequence_length=sequence_length,
        shuffle=True,
        batch_size=batch_size,
        start_index=num_test_samples)
    
    return train_data, train_dataset, val_dataset, test_dataset