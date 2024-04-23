import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd



def get_data(symbol, path):

    # Fetch stock data for Barclays PLC
    stock = yf.Ticker(symbol)
    
    today = datetime.today()
    startdate = today - timedelta(days=5900)
    yesterday = today - timedelta(days=1)

    # Get historical market data for Barclays PLC
    data = stock.history(start=startdate, end=yesterday)
    
    # Extract relevant information: Open, High, Low, Close, Volume
    stock_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

    # File save
    stock_data.to_csv(path)



def update(start_datetime, end_datetime, symbol, file_path):

    # Fetch stock data for Barclays PLC
    stock = yf.Ticker(symbol)

    # Get yesterday stock data
    data = stock.history(start=start_datetime, end=end_datetime)

    if data.empty:
        pass

    else:
        try:
            existing_data = pd.read_csv(file_path)
            existing_data['Date'] = pd.to_datetime(existing_data['Date'], utc=True)
            existing_data['Date'] = existing_data['Date'].dt.tz_localize(None).dt.date
            latest_date_in_csv = existing_data['Date'].max()
            
            # Filter new data that is greater than the latest date in CSV
            data.reset_index(inplace=True)  # Resetting index to use the 'Date' column
            data['Date'] = data['Date'].dt.date  # Ensuring 'Date' is in date format
            new_data = data[data['Date'] > latest_date_in_csv]
            
            if not new_data.empty:
                new_data = new_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                new_data.to_csv(file_path, mode='a', header=False, index=False)
                print("New data appended to the CSV.")
            else:
                print("No new data to append.")

        except FileNotFoundError:
            data.to_csv(file_path, mode='w', header=True, index=False)
            print("CSV file created with new data.")
