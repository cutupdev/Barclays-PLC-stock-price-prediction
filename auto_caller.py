
import data_collect
import schedule
import threading
import time
from datetime import datetime
from datetime import time as tm
import train
from app import PAST, FUTURE, DATA_PATH, STD_PATH, SYMBOL



def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)



def daily_update():

    print("It's 6 PM GMT now !")

    # Get the current date
    current_date = datetime.now().date()

    # Define the start and end time for the data collection window
    start_time = tm(6, 0)  # 6 AM
    end_time = tm(18, 0)  # 6 PM

    # Create the start and end datetime instances for today
    start_datetime = datetime.combine(current_date, start_time)
    end_datetime = datetime.combine(current_date, end_time)

    data_collect.update(start_datetime, end_datetime, SYMBOL, DATA_PATH)



def model_update():
    print('Model update started!')
    train.train(PAST, FUTURE, 'open', DATA_PATH, STD_PATH)
    train.train(PAST, FUTURE, 'high', DATA_PATH, STD_PATH)
    train.train(PAST, FUTURE, 'low', DATA_PATH, STD_PATH)
    train.train(PAST, FUTURE, 'close', DATA_PATH, STD_PATH)
    


# Schedule the daily update of datasets to run every day at 6 PM
schedule.every().day.at("18:00").do(daily_update)


# Schedule the weekly update of datasets to run every week
schedule.every().monday.at("11:13").do(model_update)


# Start a thread to run the scheduled tasks
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()