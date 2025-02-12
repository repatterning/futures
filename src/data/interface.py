"""Module interface.py"""
import logging

import pandas as pd

import config
import src.data.dates
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the data in focus.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Instances
        self.__streams = src.functions.streams.Streams()
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: A data sets' uniform resource identifier.
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def exc(self, stamp: str) -> pd.DataFrame:
        """

        :return:
        """

        # The data sets' uniform resource identifier
        uri = ('s3://' + self.__s3_parameters.internal + '/' +
                self.__s3_parameters.path_internal_data + f'raw/{stamp}.csv')
        self.__logger.info(uri)

        # Reading the data
        data = self.__get_data(uri=uri)
        data.info()
        self.__logger.info(data.head())

        # Return
        return data
