import logging
from typing import Optional
import requests
import time

from .._client.model import UrlInput, UrlOutput
from .storage_client import StorageClient
from .._client.client import Client

log = logging.getLogger("TitanQ")


class ManagedStorage(StorageClient):
    def __init__(self, titanq_client: Client):
        """
        Initiate the managed storage client for handling the temporary files.

        :titanq_client: titanq_client to be used to fetch temporary URL's
        """
        self._titanq_client = titanq_client
        self._urls = titanq_client.temp_storage()

    def _upload_arrays(self, bias: bytes, weights: bytes, bias_constraints: Optional[bytes], weights_constraints: Optional[bytes]):
        upload_tuple = [
            (self._urls.input.bias_file.upload, bias),
            (self._urls.input.weights_file.upload, weights),
        ]

        if bias_constraints:
            upload_tuple.append((self._urls.input.bias_constraints_file.upload, bias_constraints))

        if weights_constraints:
            upload_tuple.append((self._urls.input.weights_constraints_file.upload, weights_constraints))

        log.debug(f"Uploading files on our temporary storage")
        for url, data in upload_tuple:
            requests.put(url, data=data)


    def _input(self) -> UrlInput:
        return UrlInput(
            weights_file_name=self._urls.input.weights_file.download,
            bias_file_name=self._urls.input.bias_file.download)

    def _output(self) -> UrlOutput:
        return UrlOutput(result_archive_file_name=self._urls.output.result_archive_file.upload)

    def _wait_for_result_to_be_uploaded_and_download(self) -> bytes:
        self._wait_for_file_to_be_uploaded(self._urls.output.result_archive_file.download)
        return self._download_file(self._urls.output.result_archive_file.download)

    def _wait_for_file_to_be_uploaded(self, url: str):
        """
        Wait until the content of the file in the temporary storage is bigger
        than 0 bytes. Meaning it will wait until the file is uploaded

        :param url: Url to download the file.
        """
        response = requests.get(url)
        response.raise_for_status()
        while len(response.content) == 0:
            time.sleep(0.25)
            response = requests.get(url)
            response.raise_for_status()

    def _download_file(self, url) -> bytes:
        """
        Download file from the temporary storage

        :param url: Url to download the file.

        :return: content of the file in bytes
        """
        log.debug(f"Downloading object from the temporary storage")
        request = requests.get(url)
        return request.content

    def _delete_remote_object(self) -> None:
        log.debug("Temporary storage option does not delete any file at the moment")