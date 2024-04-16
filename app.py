from flask import * 
import predict
import data_update
import schedule
import threading
import time
from datetime import datetime
from datetime import time as tm


# Initialising flask
app = Flask(__name__) 


# Defining the route for the main() funtion
@app.route("/", methods=["POST", "GET"]) 
def main():
    # data_update.real_time_data_update()
    past, future, dates = predict.predict()
    past = past.tolist()
    past = past + [None, None, None, None, None]
    future = future.tolist()
    future = [None, None, None, None, None, None, None, None, None, past[9]] + future 
    # print("past >>>>> ", past, "future >>>>> ", future)
    temp = 0
    # data = {'past': [1,5,7,2,5,6,9,2,1,10]}
    data = {'past': past, 'future': future, 'dates': dates}
    # print(type(past))
    # print(type([1,2,3]))
    if (request.method == 'POST'):
        temp = 10
        data = {'temp': temp}

    return render_template("home.html", data = data) #rendering our home.html contained within /templates


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)


def data_collection():

    print("It's 6 PM GMT now !")

    # Get the current date
    current_date = datetime.now().date()

    # Define the start and end time for the data collection window
    start_time = tm(6, 0)  # 6 AM
    end_time = tm(18, 0)  # 6 PM

    # Create the start and end datetime instances for today
    start_datetime = datetime.combine(current_date, start_time)
    end_datetime = datetime.combine(current_date, end_time)

    data_update.real_time_data_update(start_datetime, end_datetime)
    

# Schedule the data_collection to run every day at 6 PM
schedule.every().day.at("18:00").do(data_collection)


# Start a thread to run the scheduled tasks
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()


if __name__ == "__main__": 
    
    # Running flask
    app.run(debug = True, port = 4949) 