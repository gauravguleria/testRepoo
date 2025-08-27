import login_module
import data_download_module
import backtest_module

def main_menu(kite):
    """
    Displays the main menu and handles user navigation.

    This function presents the user with a choice to download data, run a backtest,
    or exit the application. It calls the appropriate module based on the user's
    selection.

    Args:
        kite: An authenticated KiteConnect object.
    """
    # Loop indefinitely until the user chooses to exit
    while True:
        # Print the main menu options
        print("\n" + "="*20)
        print("    Main Menu")
        print("="*20)
        print("1. Download Market Data")
        print("2. Run Backtest on Strategy")
        print("3. Exit Application")
        print("="*20)
        # Prompt the user for their choice
        choice = input("Enter your choice (1-3): ")

        # Call the data download module if the user chooses '1'
        if choice == '1':
            data_download_module.download_data(kite)
        # Call the backtest module if the user chooses '2'
        elif choice == '2':
            backtest_module.run_backtest()
        # Exit the application if the user chooses '3'
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        # Handle invalid input
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    """
    The main entry point of the application.
    """
    print("--- Welcome to the Trading Application ---")
    # First, attempt to log in and get an authenticated Kite object
    kite = login_module.login()

    # If login is successful, display the main menu
    if kite:
        main_menu(kite)