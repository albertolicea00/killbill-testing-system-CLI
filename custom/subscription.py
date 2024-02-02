class Subscription:
    def __init__(self, client):
        self.client = client

    def create_subscription(self, accountId, productName, externalKey, 
                            billingPeriod="MONTHLY", priceList="DEFAULT", 
                            productCategory="BASE", user="admin", reason="", 
                            comment=""):
        # Create an subscription
        data = {"accountId":accountId,
                "externalKey":externalKey,
                "productName":productName,
                "productCategory":productCategory,
                "billingPeriod":billingPeriod,
                "priceList":priceList}
        endpoint = "1.0/kb/subscriptions"
        response = self.client.make_request("POST", endpoint, data=data, user=user,
                                        reason=reason, comment=comment)
        return response

