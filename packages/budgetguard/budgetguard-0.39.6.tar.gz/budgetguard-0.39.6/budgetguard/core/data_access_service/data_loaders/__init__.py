from .nordigen_data_loader import NordigenDataLoader
from .s3_data_loader import S3DataLoader
from .data_loader import DataLoader
from .spark_s3_data_loader import SparkS3DataLoader
from .exchange_rates_data_loader import ExchangeRatesDataLoader


def create_data_loader(data_loader_type: str) -> DataLoader:
    """
    Factory function for creating data loaders.

    :param data_loader_type: The type of data loader to create.

    :return: The data loader.
    """
    if data_loader_type == "nordigen":
        return NordigenDataLoader()
    elif data_loader_type == "s3":
        return S3DataLoader()
    elif data_loader_type == "spark_s3":
        return SparkS3DataLoader()
    elif data_loader_type == "exchange_rates":
        return ExchangeRatesDataLoader()
    else:
        raise ValueError(f"Data loader type {data_loader_type} not supported.")
