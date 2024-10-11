import os
from dotenv import load_dotenv
from openapi_client.api import *
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from custom.killbill_api_client import KillBillAPIClient


# Load environment variables from .env file
load_dotenv()

# Retrieve data from .env file
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
baseURL = os.getenv("BASE_URL")

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

config = Configuration(
    host=baseURL,
    api_key={"Killbill_Api_Key": api_key, "Killbill_Api_Secret": api_secret},
    username=username,
    password=password,
)

client = ApiClient(config)
custom_client = KillBillAPIClient(baseURL, username, password, api_key, api_secret)

subscription_api = SubscriptionApi(client)
catalog_api = CatalogApi(client)
account_api = AccountApi(client)
