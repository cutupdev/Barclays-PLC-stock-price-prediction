from flask import * 
import predict

PAST = 20
FUTURE = 5
DATA_PATH = 'datasets/barc.csv'
STD_PATH = 'datasets/financial_data.csv'
SYMBOL = 'BARC.L'
TARGET_OPEN = 'open'
TARGET_HIGH = 'high'
TARGET_LOW = 'low'
TARGET_CLOSE = 'close'



# Initialising flask
app = Flask(__name__) 



# Defining the route for the main() funtion
@app.route("/", methods=["POST", "GET"]) 
def main():

    open_past, open_future = predict.predict(TARGET_OPEN, PAST, FUTURE, STD_PATH, DATA_PATH)
    high_past, high_future = predict.predict(TARGET_HIGH, PAST, FUTURE, STD_PATH, DATA_PATH)
    low_past, low_future = predict.predict(TARGET_LOW, PAST, FUTURE, STD_PATH, DATA_PATH)
    close_past, close_future = predict.predict(TARGET_CLOSE, PAST, FUTURE, STD_PATH, DATA_PATH)

    dates = predict.getDate(DATA_PATH, PAST, FUTURE)

    open_past = open_past.tolist()
    open_past = open_past + [None] * FUTURE
    open_future = open_future.tolist()
    open_future = [None] * (PAST-1) + [open_past[PAST-1]] + open_future

    high_past = high_past.tolist()
    high_past = high_past + [None] * FUTURE
    high_future = high_future.tolist()
    high_future = [None] * (PAST-1) + [high_past[PAST-1]] + high_future

    low_past = low_past.tolist()
    low_past = low_past + [None] * FUTURE
    low_future = low_future.tolist()
    low_future = [None] * (PAST-1) + [low_past[PAST-1]] + low_future

    close_past = close_past.tolist()
    close_past = close_past + [None] * FUTURE
    close_future = close_future.tolist()
    close_future = [None] * (PAST-1) + [close_past[PAST-1]] + close_future
    
    # print("past >>>>> ", past, "future >>>>> ", future)
    temp = 0
    # data = {'past': [1,5,7,2,5,6,9,2,1,10]}
    data = {
        'open_past': open_past, 'open_future': open_future, 
        'high_past': high_past, 'high_future': high_future, 
        'low_past': low_past, 'low_future': low_future, 
        'close_past': close_past, 'close_future': close_future, 
        'dates': dates
    }
    # print(type(past))
    # print(type([1,2,3]))
    if (request.method == 'POST'):
        temp = 10
        data = {'temp': temp}

    return render_template("home.html", data = data) #rendering our home.html contained within /templates



if __name__ == "__main__": 
    
    # Running flask
    app.run(debug = True, port = 4445) 