
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


class JSONTypesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, tuple):
            return list(obj)
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='index')
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if any([isinstance(obj, int_type) for int_type in [np.int64, np.int32, np.int16, np.int8]]):
            return int(obj)
        if any([isinstance(obj, float_type) for float_type in [np.float16, np.float32, np.float64]]):
            return float(obj)
        print(type(obj))
        return json.JSONEncoder.default(self, obj)


class JSONFileBuffers:
    path: Path
    dict_type: bool

    def __init__(self, path: Path, dict_type: bool) -> None:
        self.path = path
        self.dict_type = dict_type

    def start(self):
        with open(self.path, 'w') as file:
            file.write('{' if self.dict_type else '[')

    def data_chunk(self, data: Any, key: str, encoder: json.JSONEncoder):
        value = json.dumps(data, indent=4, cls=encoder)
        with open(self.path, 'a') as file:
            if self.dict_type:
                file.write('\n')
                file.write(json.dumps(key, indent=4, cls=encoder))
                file.write(': ')
            else:
                file.write('\n')
            file.write(value)
            file.write(',')
        pass

    def end(self):
        with open(self.path, 'rb+') as file:
            file.seek(-1, 2)
            file.truncate()
        with open(self.path, 'a') as file:
            file.write('\n}' if self.dict_type else '\n]')
