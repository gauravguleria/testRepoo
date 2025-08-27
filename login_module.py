import configparser
from kiteconnect import KiteConnect
import datetime as dt
import os

def login():
    """
    Handles the login process for the Kite Connect API.

    This function first checks the 'config.ini' file for a valid, non-expired
    access token. If a token from the current day is found, it uses that
    to initialize the Kite Connect session.

    If no valid token is found, it prompts the user to go through the
    manual login flow by providing a login URL and asking for the request token.
    Upon successful authentication, it saves the new access token and the
    current timestamp to 'config.ini' for future use.

    Returns:
        KiteConnect: An authenticated KiteConnect object if login is successful,
                     otherwise None.
    """
    # Create a parser for the configuration file
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read('config.ini')

    # Retrieve API key and secret from the config file
    api_key = config['KITE']['api_key']
    api_secret = config['KITE']['api_secret']
    # Retrieve stored access token and its timestamp
    access_token = config['KITE']['access_token']
    token_timestamp_str = config['KITE']['token_timestamp']

    # Initialize the KiteConnect client with the API key
    kite = KiteConnect(api_key=api_key)

    # Check if an access token and its timestamp exist
    if access_token and token_timestamp_str:
        # Convert the timestamp string back to a datetime object
        token_timestamp = dt.datetime.strptime(token_timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        # Check if the token was generated on the same day
        if token_timestamp.date() == dt.date.today():
            try:
                # Set the access token for the KiteConnect client
                kite.set_access_token(access_token)
                print("Logged in successfully using the stored access token.")
                # Return the authenticated KiteConnect object
                return kite
            except Exception as e:
                # Handle cases where the stored token is invalid
                print(f"Failed to use stored access token: {e}. Please log in again.")
        else:
            # Inform the user that the token has expired
            print("The stored access token has expired. Please log in again.")

    # If no valid token is found, proceed with manual login
    print("Please log in using the URL below and paste your request_token here:")
    # Print the login URL for the user
    print(kite.login_url())
    # Get the request token from the user's input
    request_token = input("Enter the request_token: ")

    try:
        # Generate a new session using the request token and API secret
        data = kite.generate_session(request_token, api_secret=api_secret)
        # Extract the new access token from the response
        access_token = data["access_token"]
        # Set the new access token for the KiteConnect client
        kite.set_access_token(access_token)

        # Update the config file with the new access token and timestamp
        config['KITE']['access_token'] = access_token
        config['KITE']['token_timestamp'] = str(dt.datetime.now())
        # Write the changes back to the config file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        print("Login successful!")
        # Return the newly authenticated KiteConnect object
        return kite
    except Exception as e:
        # Handle any exceptions during the authentication process
        print(f"Authentication failed: {e}")
        return None