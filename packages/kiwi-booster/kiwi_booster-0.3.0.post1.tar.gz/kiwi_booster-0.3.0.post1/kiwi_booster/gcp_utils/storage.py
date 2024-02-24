import os
import re
import typing as tp
import urllib
from datetime import timedelta

import google.oauth2.credentials
from google.auth import impersonated_credentials
from google.cloud import storage


def get_bucket_and_path(gcs_full_path: str) -> tp.Tuple[str, str]:
    """Splits a google cloud storage path into bucket_name and the rest
    of the path without the 'gs://' at the beginning

    Args:
        gcs_full_path (str): A valid Gcloud Storage path

    Raises:
        ValueError: If input path does not start with gs://

    Returns:
        tp.Tuple[str]: Bucket name and the rest of the path
    """
    m = re.match(r"(gs://)([^/]+)/(.*)", gcs_full_path)

    if m is None:
        raise ValueError("path is not valid, it needs to start with 'gs://'")

    bucket = m.group(2)
    file_path = m.group(3)
    return bucket, file_path


def gcs_to_http(url: str) -> str:
    """
    Parses a url to a http url.

    Args:
        url (str): The url to parse.

    Returns:
        str: The http url.
    """
    return url.replace("gs://", "https://storage.cloud.google.com/")


def gcs_to_storage_search(url: str) -> str:
    """
    Parses a url to a http url.

    Args:
        url (str): The url to parse.

    Returns:
        str: The http url.
    """
    # Remove the gs:// prefix
    url = url.replace("gs://", "")
    # get the bucket
    splitted = url.split("/")
    bucket = splitted[0]
    # get the path
    path = "/".join(splitted[1:])
    path_web = urllib.parse.quote(path)
    url = f"https://console.cloud.google.com/storage/browser/{bucket};tab=objects?prefix={path_web}&forceOnObjectsSortingFiltering=false"
    return url


def generate_download_signed_url_v4(
    gcs_path: str,
    storage_client: storage.Client,
    signing_credentials: google.oauth2.credentials.Credentials,
    expiration_mins: int = 30,
) -> str:
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    url = None
    try:
        bucket, file_path = get_bucket_and_path(gcs_path)
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(file_path)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=timedelta(minutes=expiration_mins),
            # Allow GET requests using this URL.
            method="GET",
            credentials=signing_credentials,
        )
    except Exception as e:
        print(f"Error getting signed URL: {e}")

    return url


class GCSCredentials:
    """
    Class to handle the GCS credentials and signing of URLs
    """

    def __init__(self):
        credentials, project = google.auth.default()
        gcs_client = storage.Client(project=project)
        self.gcp_interface = gcs_client

        target_principal = os.getenv("TARGET_SERVICE_ACCOUNT")
        self.signing_credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=target_principal,
            target_scopes="https://www.googleapis.com/auth/devstorage.read_only",
            lifetime=10 * 60,  # validity in seconds
        )

    def gcs_to_signed_url(self, gcs_url: str) -> str:
        """
        Sign a GCS url to be accessible for 15 minutes.
        Args:
            gcs_url: The GCS url to sign.
        Returns:
            The signed URL.
        """
        return self.gcp_interface.gcs2signed(
            gcs_url, credentials=self.signing_credentials
        )
