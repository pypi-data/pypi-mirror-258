from enum import StrEnum
from pathlib import Path

DATASETS_DIRECTORY = Path(__file__).parent.parent


class ExtendedEnum(StrEnum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class LoadFormats(ExtendedEnum):
    DATAFRAME = "pandas.Dataframe"
    DICT = "dict"


class Datasets(ExtendedEnum):
    BREAST_CANCER = "breast_cancer"


class Directories(StrEnum):
    DATA_DIRECTORY = f"{DATASETS_DIRECTORY}/data"


DatasetsFiles = {
    Datasets.BREAST_CANCER: 'breast_cancer.csv'
}
