from openapi_client.models import Account
from config import account_api
import urllib3


def create_account():
    """
    Creates a new user account on the server.

    This function prompts the user to enter their name and email address via the console,
    then creates a new account with the provided information. The account is created with
    a default currency of USD. After creating the account, the function retrieves the account
    details from the server and prints the account ID.

    Steps:
    1. Prompts the user to enter their name and email address.
    2. Creates an account with the provided information and a default currency of USD.
    3. Adds the account to the server.
    4. Retrieves the account details using the external key.
    5. Prints the created account ID.

    :return: None
    """

    # Get the user's name, email address, and password from the console.
    name = input("Enter name: ")
    email = input("Enter email address: ")

    # Create account
    account = Account.from_dict(
        {"name": name, "email": email, "externalKey": name.lower(), "currency": "USD"}
    )

    # Create the account on the server.
    a = account_api.create_account_without_preload_content("admin", account)
    account: Account = account_api.get_account_by_key(external_key=name.lower())

    print(f"Created account id: {account.account_id}")
