from config import custom_client


def manage_test_plugin():
    """
    Manages the test payment plugin configuration.

    This function prompts the user to select an action via the console to configure the test payment plugin.
    The user can choose to configure the plugin for failure or success.

    Steps:
    1. Displays a menu with options to exit, configure for failure, or configure for success.
    2. Prompts the user to enter the desired action.
    3. Configures the test payment plugin based on the user's selection.

    :return: None
    """

    # Get the action from the console.
    print("--------------------------")
    print("0. Exit")
    print("1. Configure for failure")
    print("2. Configure for  success")
    action = int(input("Enter the desired action: "))

    if action == 1:
        custom_client.test_payment.config_failure()
    elif action == 2:
        custom_client.test_payment.config_success()
