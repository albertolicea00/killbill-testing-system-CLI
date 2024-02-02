class Account:
    AUDIT_NONE = "NONE"
    AUDIT_FULL = "FULL"
    AUDIT_MINIMAL = "MINIMAL"

    def __init__(self, client):
        self.client = client

    def create_account(self, data, user="admin", reason="", comment=""):
        """Creates a new account in the Knowledge Base.

        Args:
            data (dict): The data for the new account.
            user (str): The user who created the account.
            reason (str): The reason for creating the account.
            comment (str): A comment about the account creation.

        The  data  argument is a dictionary that contains the data for the new account. The following keys are required: 
        *  name : The name of the account. 
        firstNameLength : The length of the account holder's first name. 
        *  externalKey : The external key for the account. 
        email : The email address for the account holder. 
        billCycleDayLocal : The day of the month when the account is billed. 
        currency : The currency for the account. 
        parentAccountId : The ID of the parent account, if any. 
        isPaymentDelegatedToParent : Whether or not payment is delegated to the parent account. 
        referenceTime : The local time of the account creation. 
        timeZone : The time zone for the account. 
        address1 : The first line of the account holder's address. 
        address2 : The second line of the account holder's address. 
        postalCode : The postal code for the account holder's address. 
        company : The name of the account holder's company. 
        city : The city where the account holder lives. 
        state : The state where the account holder lives. 
        country : The country where the account holder lives. 
        locale : The locale for the account. 
        phone : The phone number for the account holder. 
        notes : Any notes about the account. 
        isMigrated : Whether or not the account has been migrated from another system. 
        accountBalance : The balance of the account. 
        accountCBA : The credit balance of the account. 
                Example:
        data = {
            "name": "John Doe",
            "firstNameLength": 8,
            "externalKey": external_key,
            "email": "johndoe@example.com",
            "billCycleDayLocal": 15,
            "currency": "USD",
            "parentAccountId": None,
            "isPaymentDelegatedToParent": False,
            "referenceTime": local_time_str,
            "timeZone": "America/New_York",
            "address1": "123 Main Street",
            "address2": "Apt 4B",
            "postalCode": "12345",
            "company": "ABC Company",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "locale": "en_US",
            "phone": "123-456-7890",
            "notes": "Lorem ipsum dolor sit amet.",
            "isMigrated": True,
            "accountBalance": 100.50,
            "accountCBA": 50.25
        }

        The  user  argument is the user who created the account. 
        This is used to track who created the account. 

        The  reason  argument is the reason for creating the account. 
        This is used to provide context for the account creation. 

        The  comment  argument is a comment about the account creation. 
        This is used to provide additional information about the account creation.

        Returns:
            JSON object: The details of the newly created account.
        """

        endpoint = "1.0/kb/accounts"
        return self.client.make_request("POST", endpoint, data, user=user,
                                        reason=reason, comment=comment)

    def get_account(self, external_key, accountWithBalance=False,
                    user="admin", reason="", comment="", audit=AUDIT_NONE,
                    accountWithBalanceAndCBA=False):
        endpoint = f"1.0/kb/accounts?externalKey={external_key}&accountWithBalance={str(accountWithBalance).lower()}&accountWithBalanceAndCBA={str(accountWithBalanceAndCBA).lower()}&audit={audit}"
        return self.client.make_request("GET", endpoint, None, user=user,
                                        reason=reason, comment=comment)
    
    def set_payment_method(self, accountId, user="admin", reason="", comment="", 
                           isDefault=True, pluginName="killbill-payment-test", 
                           pluginInfo={}):
        # Get the account ID
        data={"pluginName":pluginName,"pluginInfo":pluginInfo}
        endpoint = f"1.0/kb/accounts/{accountId}/paymentMethods?isDefault={str(isDefault).lower()}"
        return self.client.make_request("POST", endpoint, data, user=user,
                                        reason=reason, comment=comment)
    
    def get_id(self, external_key):
        # Get the accountId by the externalKey
        response = self.get_account(external_key)
        return response.json()['accountId']
