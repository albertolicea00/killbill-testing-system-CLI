from openapi_client.models import PaymentMethod
from config import account_api


def add_payment_method():
    """
    Adds a test payment method to a user's account.

    This function creates a test payment method using the 'killbill-payment-test' plugin
    and adds it to the specified user's account. The account ID is obtained from the console input.

    Steps:
    1. Creates a test payment method using the 'killbill-payment-test' plugin.
    2. Prompts the user to enter the account ID.
    3. Adds the payment method to the user's account on the server, setting it as the default payment method.

    :return: None
    """

    testMethod = PaymentMethod.from_dict(
        {
            "pluginName": "killbill-payment-test",
            "pluginInfo": {},
        }
    )

    # Get the user's payment method information from the console.
    account_id = input("Enter the account ID: ")

    # Add the payment method to the user's account on the server.
    account_api.create_payment_method_without_preload_content(
        account_id,
        "admin",
        testMethod,
        is_default=True,
    )
