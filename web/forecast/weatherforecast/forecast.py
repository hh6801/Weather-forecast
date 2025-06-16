import joblib
from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import copy

model = load_model("Bi_LSTM.h5")
filename = 'Data.csv'
n_days_for_prediction = 7

def forecast(filename, model, n_days_for_prediction):

    # Load dữ liệu từ file CSV
    data = pd.read_csv(filename)

    # Chọn window và thuộc tính
    window_size = 7
    features = ["Max Temp", "Avg Temp", "Min Temp",
                "Max Dew Point", "Avg Dew Point", "Min Dew Point"]
    target = 'Avg Temp'

    # Chuẩn bị dữ liệu
    x = data[features].values
    y = data[target].values
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, shuffle=False)
    # Chuẩn hóa dữ liệu
    scaler = MinMaxScaler()
    scaler = scaler.fit(x_train)
    x_test = scaler.transform(x_test)

    testX = []
    for i in range(window_size, len(x_test)+1):
        testX.append(x_test[i - window_size:i, :])
    testX = np.array(testX)

    window_for_predict = testX[-1:]
    predicted_future = []

    pred = model.predict(testX)
    prediction_copies = np.repeat(pred, len(features), axis=-1)
    predicted = scaler.inverse_transform(prediction_copies)[:,features.index(target)]
    r2 = r2_score(y_test[6:], predicted)

    for i in range(0, n_days_for_prediction):
        value_predicted = model.predict(window_for_predict)
        test_model = copy.copy(model)
        if (check_train(test_model, window_for_predict, value_predicted, testX, y_test[6:],scaler,features,target) > r2):
            print("change")
            model.fit(window_for_predict,value_predicted, epochs=5, batch_size=64, verbose=0, shuffle=False)
        
        value_copy = np.repeat(value_predicted, len(features), axis=-1)
        result_predicted = scaler.inverse_transform(value_copy)
        predicted_future = np.append(predicted_future,result_predicted[:,features.index(target)], axis=0)
        window_for_predict = np.delete(window_for_predict, 0, axis=1)
        window_for_predict = np.append(window_for_predict,np.reshape(value_copy, (1, 1, len(features))), axis=1)

    return predicted_future


def check_train(model, train_x, train_y, x_test, y_test, scaler, features, target):
    model.fit(train_x, train_y, epochs=5,
                batch_size=64, verbose=0, shuffle=False)
    model.reset_states()
    pred = model.predict(x_test)
    prediction_copies = np.repeat(pred, len(features), axis=-1)
    predicted = scaler.inverse_transform(prediction_copies)[
        :, features.index(target)]
    check = r2_score(y_test, predicted)
    return check
