""" 
This Python module includes functionality to make a GET request to a Killbill API endpoint and retrieve account information. It utilizes the following dependencies: os, dotenv, requests, and base64. 
 
To use this module, follow these steps: 
1. Install the required dependencies by running  pip install os dotenv requests base64 . 
2. Create a .env file with the following data:
    BASE_URL=http://10.240.30.65:8080
    API_KEY=<ApiKey>
    API_SECRET=<ApiSecret>
    USER_NAME=<user>
    PASSWORD=<password>
3. Edit the external_key variable with any random string
"""
from dotenv import load_dotenv
import os
from openapi_client.models import Account, Subscription
from openapi_client.api_client import ApiClient
from openapi_client.api import AccountApi, SubscriptionApi
from openapi_client.configuration import Configuration

# Load environment variables from .env file
load_dotenv()

# Retrieve data from .env file
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
baseURL = os.getenv('BASE_URL')

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

config = Configuration(host=baseURL, api_key={'Killbill_Api_Key':api_key, 
                                              'Killbill_Api_Secret': api_secret}, 
                                              username=username, password=password) 
client = ApiClient(config)
# Create an instance of the AccountApi class
account_api = AccountApi(client)

print(account_api.get_account('90792be6-0a24-4de1-9c43-3428c00451d6'))