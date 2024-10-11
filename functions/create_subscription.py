from openapi_client.models import Subscription
from config import subscription_api


def create_subscription():
    """
    Creates a new subscription for a user's account on the server.

    This function prompts the user to enter the account ID, product name, and external key via the console,
    then creates a new subscription with the provided information. The subscription is created with a default
    billing period of MONTHLY, price list of DEFAULT, and product category of BASE.

    Steps:
    1. Prompts the user to enter the account ID, product name, and external key.
    2. Creates a subscription with the provided information and default settings.
    3. Adds the subscription to the user's account on the server.

    :return: None
    """
    # Get the user's subscription information from the console.
    account_id = input("Enter the account ID: ")
    productName = input("Enter the product name: ")
    externalKey = input("Enter the external key: ")

    sub = Subscription.from_dict(
        {
            "accountId": account_id,
            "externalKey": externalKey,
            "productName": productName,
            "billingPeriod": "MONTHLY",
            "priceList": "DEFAULT",
            "productCategory": "BASE",
        }
    )

    # Create the subscription on the server.
    subscription_api.create_subscription_without_preload_content("admin", sub)
