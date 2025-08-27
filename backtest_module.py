import pandas as pd
from strategies.three_red_two_green import three_red_two_green
import os

def run_backtest():
    """
    Runs a backtest using the downloaded data and the specified trading strategy.

    This function loads the market data from 'data/nifty_data.csv', applies the
    'three_red_two_green' strategy to it, and then prints the results,
    including the total number of matches and the specific timestamps of each match.
    """
    # Define the path to the data file
    data_file = 'data/nifty_data.csv'
    # Check if the data file exists before proceeding
    if not os.path.exists(data_file):
        print(f"Data file not found at {data_file}. Please download the data first from the main menu.")
        return

    # Load the data from the CSV file into a pandas DataFrame
    df = pd.read_csv(data_file)
    print("Running backtest for the '3 red candles, 2 green candles' strategy...")

    # Call the strategy function to find all pattern matches in the data
    matches = three_red_two_green(df)

    # Check if any matches were found
    if matches:
        # Print the total number of matches found
        print(f"Found {len(matches)} matches for the pattern.")
        print("The pattern was found at the following dates and times:")
        # Iterate through the list of match indices and print the details
        for match_index in matches:
            # Use .iloc to get the row at the specific index and print Date and Time
            print(f"  - Date: {df.iloc[match_index]['Date']}, Time: {df.iloc[match_index]['Time']}")
    else:
        # If no matches were found, inform the user
        print("No matches were found for the specified pattern in the dataset.")