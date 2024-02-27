import pandas as pd

from .constants import Directories, LoadFormats, Datasets, DatasetsFiles

__all__ = [
    'load_dataset'
]


def load_dataset(dataset: str, output_format: str = 'pandas.Dataframe'):
    """
    Abstract function to load a dataset.
    :param dataset: Dataset tag.
    :param output_format: Output format of data. It can be: pandas.Dataframe or dict.
    :return: Dataset in the desired format.
    """
    data = pd.read_csv(f"{Directories.DATA_DIRECTORY}/{_get_dataset_directory(dataset)}")

    if output_format == LoadFormats.DATAFRAME:
        return data
    elif output_format == LoadFormats.DICT:
        return data.to_dict()
    else:
        raise NotImplementedError(
            f"Output format {output_format} is not implemented. The available formats are: {LoadFormats.list()}."
        )


def _get_dataset_directory(dataset: str):

    if dataset in Datasets:
        dataset_tag = Datasets(dataset)
        return DatasetsFiles.get(dataset_tag)
    else:
        raise NotImplementedError(f'Dataset {dataset} is not implemented. The available dataset are: {Datasets.list()}')
