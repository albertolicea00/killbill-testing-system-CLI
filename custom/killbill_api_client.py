import json
import requests
from base64 import b64encode

# Import functionalities
from .account import Account
from .catalog import Catalog
from .clock import Clock
from .subscription import Subscription
from .test_payment import TestPayment


class KillBillAPIClient:
    def __init__(self, base_url, username, password, api_key, api_secret):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.api_key = api_key
        self.api_secret = api_secret

        # Load functionalities
        self.account = Account(self)
        self.catalog = Catalog(self)
        self.clock = Clock(self)
        self.subscription = Subscription(self)
        self.test_payment = TestPayment(self)

    def _basic_auth(self):
        token = b64encode(f"{self.username}:{self.password}".encode(
            'utf-8')).decode("ascii")
        return f'Basic {token}'

    def make_request(self, method, endpoint, data=None,
                     user="admin", reason="", comment="",
                     content_type="application/json"):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Accept': 'application/json',
            'Authorization': self._basic_auth(),
            "X-Killbill-ApiKey": self.api_key,
            "X-Killbill-ApiSecret": self.api_secret,
            "X-Killbill-CreatedBy": user,
            "X-Killbill-Reason": reason,
            "X-Killbill-Comment": comment,
            "Content-Type": content_type
        }

        # Convert dict into json
        if content_type == "application/json":
            data=json.dumps(data)

        response = requests.request(
            method, url, headers=headers, data=data)
        response.raise_for_status()
        return response
