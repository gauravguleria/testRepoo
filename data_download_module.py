import configparser
from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta
import os

def download_data(kite: KiteConnect):
    """
    Downloads historical market data for the instrument specified in the config file.

    This function reads data parameters from 'config.ini', including the instrument
    token, time interval, and time period. It handles API limitations by
    downloading data in smaller chunks if the requested period is too long.

    The downloaded data is formatted and saved into a CSV file within a structured
    folder system.

    Args:
        kite (KiteConnect): An authenticated KiteConnect object.
    """
    # Create a parser for the configuration file
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read('config.ini')

    # Retrieve data parameters from the config file
    instrument_token = int(config['DATA']['instrument_token'])
    instrument_name = config['DATA']['instrument_name']
    time_interval = config['DATA']['time_interval']
    time_period_years = int(config['DATA']['time_period_years'])
    output_folder = config['DATA']['output_folder']
    start_date_str = config['DATA']['start_date']

    # Define the date range for data download
    to_date = datetime.now().date()
    # Convert the start date string to a date object
    from_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    # Ensure the from_date does not exceed the specified year period
    if (to_date - from_date).days > (time_period_years * 365):
        from_date = to_date - timedelta(days=time_period_years * 365)

    print(f"Downloading {time_period_years} years of {time_interval} data for {instrument_name}...")

    # A list to store all the downloaded data records
    all_data = []
    # Set the starting point for the data download loop
    current_from = from_date

    # Loop to download data in chunks to avoid API limits (e.g., 100 days per request)
    while current_from < to_date:
        # Define the end of the current chunk
        chunk_to = min(current_from + timedelta(days=100), to_date)
        try:
            # Fetch historical data for the current chunk
            records = kite.historical_data(instrument_token, current_from, chunk_to, time_interval)
            # If data is returned, add it to our list
            if records:
                all_data.extend(records)
        except Exception as e:
            # Handle any errors during the data fetch
            print(f"Error fetching data from {current_from} to {chunk_to}: {e}")
        
        # Move to the next chunk
        current_from = chunk_to + timedelta(days=1)

    # If no data was downloaded, exit the function
    if not all_data:
        print("No data was downloaded. Please check your parameters.")
        return

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(all_data)
    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    # Create separate 'Time' and 'Date' columns
    df['Time'] = df['date'].dt.strftime('%H:%M:%S')
    df['Date'] = df['date'].dt.strftime('%Y-%m-%d')
    # Select and reorder the columns
    df = df[['Date', 'Time', 'open', 'high', 'low', 'close', 'volume']]
    # Rename columns to have a consistent format
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

    # Create the main output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a subfolder for the specific instrument
    instrument_folder = os.path.join(output_folder, instrument_name.replace(' ', '_'))
    if not os.path.exists(instrument_folder):
        os.makedirs(instrument_folder)

    # Define the filename for the downloaded data
    retrieval_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{instrument_name.replace(' ', '_')}_{time_interval}_{time_period_years}years_{retrieval_date}.csv"
    file_path = os.path.join(instrument_folder, file_name)
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)
    print(f"Data successfully saved to {file_path}")

    # Also save a generic file for easy access during backtesting
    generic_file_path = os.path.join(output_folder, 'nifty_data.csv')
    df.to_csv(generic_file_path, index=False)
    print(f"Generic data file for backtesting saved to {generic_file_path}")