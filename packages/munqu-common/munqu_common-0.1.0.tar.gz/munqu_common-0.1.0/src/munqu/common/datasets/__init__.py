from .utils.utils import load_dataset as _load_dataset
from .utils.constants import Datasets as _Datasets

__all__ = [
    'load_breast_cancer'
]


def load_breast_cancer(output_format: str = 'pandas.Dataframe'):
    """
    Load Breast Cancer dataset.
    :return: Breast Cancer dataset in the desired format.
    """
    return _load_dataset(dataset=_Datasets.BREAST_CANCER, output_format=output_format)
