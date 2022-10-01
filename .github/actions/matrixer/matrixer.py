import json
from pathlib import Path
from typing import (
    TypedDict,
)
import sys

import yaml
from pydantic import BaseModel, Field


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


def get_data(spec: str) -> dict:
    data = yaml.safe_load(str(spec))
    if isinstance(data, str):
        data = yaml.safe_load(Path(data).read_text())
    assert isinstance(data, dict)
    return data


def main(source: str, pv=None, strategy=False):
    data = get_data(source)

    if pv:
        data = {"_key": pv, **data[pv]}

    matrix = to_matrix(data)
    strategy = to_strategy(matrix)

    set_output("matrix", matrix)
    set_output("strategy", strategy)
    # print(json.dumps(out_data, indent=4))


def set_output(name, data):
    out = json.dumps(data)
    print(f"::set-output name={name}::{out}")


if __name__ == '__main__':
    data = sys.argv[1]
    try:
        pv = sys.argv[2]
    except IndexError:
        pv = None
    main(
        data,
        pv=pv,
        strategy=True,
    )