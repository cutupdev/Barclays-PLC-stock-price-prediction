import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers, initializers, regularizers
import gen_dataset



def train(past, future, target, data_path, std_path):

    sequence_length = past

    train_data, train_dataset, val_dataset, test_dataset = gen_dataset.generate(past, future, target, data_path, std_path)

    # Model structure
    inputs = keras.Input(shape=(sequence_length, train_data.shape[-1]))
    # x = layers.LSTM(32, 
    #                 recurrent_dropout=0.1, 
    #                 activation="tanh", 
    #                 return_sequences = True,)(inputs)
    x = layers.LSTM(32, 
                    recurrent_dropout=0.1, 
                    activation="tanh", )(inputs)
    x = layers.Flatten()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(1, activation="tanh")(x)
    model = keras.Model(inputs, outputs)

    # Save the best model during training
    callbacks = [
        keras.callbacks.ModelCheckpoint("models/" + target + ".keras",          
                                        save_best_only=True)
    ] 

    # Model train
    model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    history = model.fit(train_dataset,
                        epochs=50,
                        validation_data=val_dataset,
                        callbacks=callbacks)

    model = keras.models.load_model("jena_dense.keras") # Load saved model

    print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}") # test the performance of the model

    # Model training check
    loss = history.history["mae"]
    val_loss = history.history["val_mae"]
    epochs = range(1, len(loss) + 1)
    plt.figure()
    plt.plot(epochs, loss, "bo", label="Training MAE")
    plt.plot(epochs, val_loss, "b", label="Validation MAE")
    plt.title("Training and validation MAE")
    plt.legend()
    plt.show()