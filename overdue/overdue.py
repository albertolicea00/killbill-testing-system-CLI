""" 
This Python module reproduces the example in:
https://docs.killbill.io/latest/overdue#_testing_the_system

It utilizes the following dependencies: os, dotenv, requests, and base64. 
It is also based on the client library in:
https://pinkzebra.visualstudio.com/pz_KillBill/_git/pz_KillBill?path=/client/killbill_api_client.py&version=GBmaster
 
To use this module, follow these steps: 
1. Install the required dependencies by running  pip install os dotenv requests base64 . 
2. Create a .env file with the following data:
    BASE_URL=http://10.240.30.65:8080
    API_KEY=<ApiKey>
    API_SECRET=<ApiSecret>
    USER_NAME=<user>
    PASSWORD=<password>
3. Create the tables in the database using:
    https://github.com/killbill/killbill-payment-test-plugin/blob/master/src/main/resources/ddl.sql
4. Intsall the payment-test plugin:
    kpm install_java_plugin payment-test
    systemctrl restart tomcat
"""

import os
import sys
import json
from dotenv import load_dotenv
from openapi_client.models import Account, PaymentMethod, Subscription
from openapi_client.api_client import ApiClient
from openapi_client.api import AccountApi, CatalogApi, SubscriptionApi

from openapi_client.configuration import Configuration
from custom.killbill_api_client import KillBillAPIClient


# try:
#     # Create an subscription
#     killbill_client.subscription.create_subscription(accountId, "Movies", "s1_arthur")
# except:
#     pass

# # Move the clock to reach end of trial (10 days ahead) and see first payment:
# killbill_client.clock.forward(days=10)


# Load environment variables from .env file
load_dotenv()

# Retrieve data from .env file
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
baseURL = os.getenv('BASE_URL')

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

# Create a custom Killbill client for clock management
custom_client = KillBillAPIClient(
    baseURL, username, password, api_key, api_secret)

config = Configuration(host=baseURL, api_key={'Killbill_Api_Key':api_key, 
                                            'Killbill_Api_Secret': api_secret}, 
                                            username=username, password=password) 
client = ApiClient(config)
# Create an instance of the AccountApi class
account_api = AccountApi(client)

def main():
    while True:
        run()

def run():
    # Print the menu options to the console.
    print("=========== Select an action: ============")
    print(json.loads(custom_client.clock.get_current_time().content)['currentUtcTime'])
    print("0. Exit")
    print("1. Upload catalog")
    print("2. Create account")
    print("3. Add payment method")
    print("4. Create subscription")
    print("5. Change the clock")
    print("6. Configure Payment Test Plugin")

    # Get the user's selection from the console.
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

def upload_catalog():
    catalog_api = CatalogApi(client)

    # Get the path to the catalog file from the user.
    catalog_path = input("Enter the path to the catalog file: ")

    # Delete the old catalog
    catalog_api.delete_catalog("admin")

    # Upload the catalog contents to the server.
    # Open the catalog file.
    with open(catalog_path, "r") as f:
        # Read the catalog file contents.
        catalog_contents = f.read()
        catalog_api.upload_catalog_xml("admin", catalog_contents)
    
def create_account():
    # Get the user's name, email address, and password from the console.
    name = input("Enter name: ")
    email = input("Enter email address: ")
    # Create account
    account = Account.from_dict({
        "name": name,
        "email": email,
        "externalKey": name.lower(),
        "currency": "USD"})
    
    # Create the account on the server.
    account_api.create_account_without_preload_content("admin", account)
    account: Account = account_api.get_account_by_key(external_key=name.lower())

    print(f"Created account id: {account.account_id}")


def add_payment_method():
    testMethod = PaymentMethod.from_dict({'pluginName':"killbill-payment-test", 
                           'pluginInfo':{}})
    # Get the user's payment method information from the console.
    account_id = input("Enter the account ID: ")

    # Add the payment method to the user's account on the server.
    account_api.create_payment_method_without_preload_content(account_id, "admin", testMethod, is_default=True)

def create_subscription():
    subscription_api=SubscriptionApi(client)
    # Get the user's subscription information from the console.
    account_id = input("Enter the account ID: ")
    productName = input("Enter the product name: ")
    externalKey = input("Enter the external key: ")

    sub = Subscription.from_dict({"accountId": account_id,
                            "externalKey": externalKey,
                            "productName": productName,
                            'billingPeriod':"MONTHLY", 
                            'priceList':"DEFAULT",
                            'productCategory':"BASE"
                            })

    # Create the subscription on the server.
    subscription_api.create_subscription_without_preload_content("admin", sub)

def change_clock():
    # Get the new clock time from the console.
    new_clock_time = input("Enter the new clock time: ")

    # Change the clock on the server.
    custom_client.clock.set_date(new_clock_time)


def manage_test_plugin():
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



if __name__ == "__main__":
    main()