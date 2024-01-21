#https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-visual-studio-code#authenticate-to-azure-and-authorize-access-to-blob-data

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os
import uuid

try:
    account_url = "https://mwecfsfiles.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    # # Create a local directory to hold blob data
    # local_path = "./data"
    # os.mkdir(local_path)

    # # Create a file in the local data directory to upload and download
    # local_file_name = str(uuid.uuid4()) + ".txt"
    # upload_file_path = os.path.join(local_path, local_file_name)

    # # Write text to the file
    # file = open(file=upload_file_path, mode='w')
    # file.write("Hello, World!")
    # file.close()

    local_file_name = "test.pdf"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container='files', blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=local_file_name, mode="rb") as data:
        blob_client.upload_blob(data)


except Exception as ex:
    print('Exception:')
    print(ex)