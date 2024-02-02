import datetime

class TestPayment:
    def __init__(self, client):
        self.client = client

    def config_failure(self, user="admin", reason="", comment=""):
        endpoint = "plugins/killbill-payment-test/configure"
        data = {"CONFIGURE_ACTION":"ACTION_RETURN_PLUGIN_STATUS_ERROR"}
        return self.client.make_request("POST", endpoint, user=user,
                                        reason=reason, comment=comment, data=data)

    def config_success(self, user="admin", reason="", comment=""):
        endpoint = "plugins/killbill-payment-test/configure"
        data = {"CONFIGURE_ACTION":"ACTION_CLEAR"}
        return self.client.make_request("POST", endpoint, user=user,
                                        reason=reason, comment=comment, data=data)