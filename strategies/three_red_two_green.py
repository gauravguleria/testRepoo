import pandas as pd

def three_red_two_green(data: pd.DataFrame):
    """
    Identifies the '3 red candles followed by 2 green candles' pattern.

    This function iterates through the provided DataFrame and checks for a specific
    candlestick pattern: three consecutive red candles (close < open) followed by
    two consecutive green candles (close > open).

    Args:
        data (pd.DataFrame): A DataFrame containing market data with 'Open' and
                             'Close' columns.

    Returns:
        list: A list of indices from the DataFrame where the end of the
              pattern is detected.
    """

    """=== 1. Print Strategy Logic === """
    print("Strategy Logic:")
    print("3 consecutive red candles (Close < Open)")
    print("Followed immediately by 2 consecutive green candles (Close > Open)")
    print("When pattern occurs → Trigger notification")
    print("=" * 60)


    data.columns = [col.strip() for col in data.columns]  # remove any extra spaces
    # Determine candle color
    data['Color'] = data.apply(lambda row: 'Red' if row['Close'] < row['Open'] else 'Green', axis=1)
    

    # A list to store the indices of matched patterns
    matches = []
    """=== 4. Process each day separately ==="""
    for date in data['Date'].unique():
        day_data = data[data['Date'] == date].reset_index(drop=True)
        if len(day_data) < 5:
            continue  # skip days with less than 5 candles

        for i in range(len(day_data) - 4):
            if (day_data.loc[i, 'Color'] == 'Red' and
                day_data.loc[i+1, 'Color'] == 'Red' and
                day_data.loc[i+2, 'Color'] == 'Red' and
                day_data.loc[i+3, 'Color'] == 'Green' and
                day_data.loc[i+4, 'Color'] == 'Green'):
              

                first_red_time = day_data.loc[i, 'Time']
                last_green_time = day_data.loc[i+4, 'Time']
                print(f"{date} | First Red Candle:{first_red_time} | Last Green Candle:{last_green_time}")

"""
day_data.loc[i, 'Color'] == 'Red' and
                day_data.loc[i+1, 'Color'] == 'Red' and
                day_data.loc[i+2, 'Color'] == 'Red' and
                day_data.loc[i+3, 'Color'] == 'Green' and
                day_data.loc[i+4, 'Color'] == 'Green'):
"""


