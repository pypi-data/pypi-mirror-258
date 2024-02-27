from enum import Enum, auto


class ModelType(Enum):
    alpha = auto()
    portfolio = auto()


class ModelConfig(Enum):
    alpha = {"class_name": "Alpha", "file_name": "am.py"}
    portfolio = {"class_name": "Portfolio", "file_name": "pf.py"}

    @property
    def class_name(self):
        return self.value["class_name"]

    @property
    def file_name(self):
        return self.value["file_name"]
