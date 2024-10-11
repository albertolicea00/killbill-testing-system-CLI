from config import custom_client


def change_clock():
    """
    Changes the server clock to a new specified time.

    This function prompts the user to enter a new clock time via the console
    and then updates the server clock to the specified time.

    Steps:
    1. Prompts the user to enter the new clock time.
    2. Updates the server clock with the new time using the custom client.

    :return: None
    """

    # Get the new clock time from the console.
    new_clock_time = input("Enter the new clock time: ")

    # Change the clock on the server.
    custom_client.clock.set_date(new_clock_time)
