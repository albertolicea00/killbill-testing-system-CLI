from config import catalog_api


def upload_catalog():
    """
    Uploads a new catalog to the server.

    This function prompts the user to enter the path to the catalog file via the console,
    deletes the old catalog on the server, and uploads the new catalog contents.

    Steps:
    1. Prompts the user to enter the path to the catalog file.
    2. Deletes the old catalog on the server.
    3. Reads the contents of the catalog file.
    4. Uploads the catalog contents to the server.

    :return: None
    """
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
