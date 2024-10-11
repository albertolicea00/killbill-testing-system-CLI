import sys
import json
from config import custom_client

from functions.upload_catalog import upload_catalog
from functions.create_account import create_account
from functions.add_payment_method import add_payment_method
from functions.create_subscription import create_subscription
from functions.change_clock import change_clock
from functions.manage_test_plugin import manage_test_plugin

# sys.path.insert(0, "[YOUR-ABSOLUTE-PATH]/killbill-testing-system-CLI/")


def main():
    """
    Main function to execute various actions based on user selection.

    This function displays a menu with options for different actions, prompts the user to select an action,
    and then executes the corresponding function. The available actions include uploading a catalog, creating
    an account, adding a payment method, creating a subscription, changing the clock, and configuring the
    payment test plugin.

    Steps:
    1. Displays the current UTC time.
    2. Prints the menu options to the console.
    3. Prompts the user to enter their selection.
    4. Executes the selected action based on the user's input.

    Available actions:
    0. Exit the program.
    1. Upload catalog.
    2. Create account.
    3. Add payment method.
    4. Create subscription.
    5. Change the clock.
    6. Configure Payment Test Plugin.

    :return: None
    """

    print("=========== Select an action: ============")
    print(json.loads(custom_client.clock.get_current_time().content)['currentUtcTime'])
    print("0. Exit")
    print("1. Upload catalog")
    print("2. Create account")
    print("3. Add payment method")
    print("4. Create subscription")
    print("5. Change the clock")
    print("6. Configure Payment Test Plugin")
    selection = int(input("Enter your selection: "))

    # Execute the selected action.
    if selection == 0:
        # Exit the program.
        sys.exit(0)
    elif selection == 1:
        upload_catalog()
    elif selection == 2:
        create_account()
    elif selection == 3:
        add_payment_method()
    elif selection == 4:
        create_subscription()
    elif selection == 5:
        change_clock()
    elif selection == 6:
        manage_test_plugin()

if __name__ == "__main__":
    while True:
        main()