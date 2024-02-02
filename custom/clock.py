import datetime

class Clock:
    def __init__(self, client):
        self.client = client

    def get_current_time(self, user="admin", reason="", comment=""):
        endpoint = "1.0/kb/test/clock"
        return self.client.make_request("GET", endpoint, user=user,
                                        reason=reason, comment=comment)

    def forward(self, days, user="admin", reason="", comment=""):
        json_data = self.get_current_time().json()
        current_utc_time = datetime.datetime.strptime(json_data['currentUtcTime'], 
                                                      '%Y-%m-%dT%H:%M:%S.%fZ')

        final_date = current_utc_time+datetime.timedelta(days=days)
        return self.set_date(final_date.date())

    def set_date(self, date, user="admin", reason="", comment=""):
        # date_str=date.strftime("%Y-%m-%d")
        endpoint = f"1.0/kb/test/clock?requestedDate={date}"
        return self.client.make_request("POST", endpoint, user=user,
                                        reason=reason, comment=comment)
