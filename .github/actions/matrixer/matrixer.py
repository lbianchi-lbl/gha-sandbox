from collections import ChainMap
import json
from pathlib import Path
from typing import (
    TypedDict,
)
import sys

import yaml


class Matrix(TypedDict):
    key: str
    include: list[dict]


class Strategy(TypedDict):
    matrix: Matrix


def to_matrix(data: dict) -> Matrix:
    data = dict(data)
    pk = list(data.keys())[0]
    pv = data.pop(pk)
    return {
        pk: [pv],
        "include": [
            {
                pk: pv,
                **data
            }
        ]
    }


def to_strategy(matrix: Matrix, **kwargs) -> Strategy:
   return {
        "matrix": matrix,
        "fail-fast": True,
   }


def set_output(name, data):
    out = json.dumps(data)
    print(f"::set-output name={name}::{out}")


def construct_include(
        loader: yaml.SafeLoader,
        node: yaml.Node,
        keypath_sep: str = ":",
        keypath_metakey: str = "_key",
    ):
    content = loader.construct_scalar(node)
    path, _, keypath = content.partition(keypath_sep)
    path = Path(path)
    path_data = yaml.safe_load(path.read_text())
    if keypath:
        path_data = {**{keypath_metakey: keypath}, **path_data[keypath]}
    return path_data


yaml.add_constructor("!include", construct_include, yaml.SafeLoader)


def get_data(source: str) -> dict:
    docs_data = list(yaml.safe_load_all(source))
    data_updated_first_to_last = ChainMap(*docs_data[::-1])
    return dict(data_updated_first_to_last)


def main(source: str):
    data = get_data(source)
    matrix = to_matrix(data)
    strategy = to_strategy(matrix)

    set_output("matrix", matrix)
    set_output("strategy", strategy)


if __name__ == '__main__':
    data = sys.argv[1]
    main(data)
