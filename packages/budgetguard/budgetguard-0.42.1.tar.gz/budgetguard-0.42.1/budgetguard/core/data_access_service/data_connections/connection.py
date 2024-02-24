from abc import ABC, abstractmethod
import requests
from loguru import logger
import os
from enum import Enum


class Connection(ABC):
    class __Platform__(Enum):
        LOCAL = "local"
        EMR = "emr"

    def __init__(self) -> None:
        """
        Constructor for Pipeline class.
        """
        self.platform = self.__set_platform__()

    def __set_platform__(self) -> str:
        """
        Sets the platform.
        """
        if "EMR_CLUSTER_ID" in os.environ:
            return self.__Platform__.EMR
        else:
            return self.__Platform__.LOCAL

    @abstractmethod
    def connect(self):
        """
        Base method for connecting to the data source.
        """
        raise NotImplementedError()

    def request(
        self,
        url: str,
        method: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """
        Method to make a request to a given url.

        :param url: The url to make the request to.
        :param method: The HTTP method to use.
        :param params: The parameters to send with the request.
        :param data: The data to send
        :param headers: The headers to send with the request.

        :return: The response object.
        """
        logger.info(f"Making {method} request to {url}...")
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error making request to {url}: {e}")
            raise e
