import numpy as np

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Type, Union


from .._client.model import S3Input, S3Output, UrlInput, UrlOutput


class StorageClient(ABC):
    def __init__(self):
        pass

    def temp_files_manager(self, bias: np.ndarray, weights: np.ndarray) -> Type["TempFileManager"]:
        """'
        Creates and returns a context manager that will be handling the temporary file management

        :param bias: bias numpy array
        :param weights: weights numpy array
        """
        return TempFileManager(self, bias, weights)

    @abstractmethod
    def _input(self) -> Union[S3Input, UrlInput]:
        """
        Returns the api model for the input of the solve request

        :return: either the s3 or the url input
        """

    @abstractmethod
    def _output(self) -> Union[S3Output, UrlOutput]:
        """
        Returns the api model for the output of the solve request

        :return: either the s3 or the url output
        """

    @abstractmethod
    def _upload_arrays(self, bias: bytes, weights: bytes):
        """
        Uploads .npy arrays (bias and weights) to the storage client

        :param bias: bias array in bytes
        :param weights: weights array in bytes
        """

    @abstractmethod
    def wait_for_result_to_be_uploaded_and_download(self) -> bytes:
        """
        Wait until a file is uploaded on the storage client and download it

        :return: content of the result file in bytes
        """

    @abstractmethod
    def _delete_remote_object(self) -> None:
        """
        Deletes a remote object on the storage client
        """

class TempFileManager():
    """
    Context manager handling the upload and download to a temporary storage
    """
    def __init__(
        self,
        storage_client: StorageClient,
        bias: np.ndarray,
        weights: np.ndarray
    ) -> None:
        """
        :param storage_client: storage client that will handle uploads, downloads and generating api models
        :param bias: bias numpy array
        :param weights: weights numpy array
        """

        super().__init__()
        self._storage_client = storage_client
        self._bias = bias
        self._weights = weights

    def __enter__(self) -> Type["TempFileManager"]:
        self._storage_client._upload_arrays(
            self._to_bytes(self._bias),
            self._to_bytes(self._weights))
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._storage_client._delete_remote_object()

    def input(self) -> Union[S3Input, UrlInput]:
        return self._storage_client._input()

    def output(self) -> Union[S3Output, UrlOutput]:
        return self._storage_client._output()

    def download_result(self):
        return self._storage_client.wait_for_result_to_be_uploaded_and_download()

    def _to_bytes(self, array: np.ndarray) -> bytes:
        """
        :return: numpy array as bytes
        """
        buffer = BytesIO()
        np.save(buffer, array)
        return buffer.getvalue()