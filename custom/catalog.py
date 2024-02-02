import xml.etree.ElementTree as ET
from datetime import datetime

class Catalog:
    def __init__(self, client):
        self.client = client

    def delete_catalog(self, user="admin", reason="", comment=""):
        endpoint = "1.0/kb/catalog"
        return self.client.make_request("DELETE", endpoint, user=user,
                                        reason=reason, comment=comment)

    def upload_catalog(self, xml_file, updateEffectiveDate=True, user="admin", reason="", comment=""):

        # Parse the XML file
        tree = ET.parse(xml_file)

        # Get the root element of the XML
        root = tree.getroot()

        if updateEffectiveDate:
            # Get the current datetime
            current_datetime = datetime.now().isoformat()

            # Update the effectiveDate element with the current datetime
            effective_date_element = root.find('effectiveDate')
            effective_date_element.text = current_datetime

        # Convert the XML content to a string and store it in the payload variable
        payload = ET.tostring(root, encoding='utf-8').decode('utf-8')

        endpoint = "1.0/kb/catalog/xml"
        return self.client.make_request("POST", endpoint, payload, user=user,
                                        reason=reason, comment=comment, content_type="text/xml")
