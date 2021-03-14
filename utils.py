import json
import typing as tp


TListMatrix = tp.List[tp.List[bool]]


def read_bool_matrices(file_name: str) -> tp.Tuple[TListMatrix, TListMatrix]:
    with open(file_name, "r") as file:
        matrices = json.load(file)
    return matrices["left"], matrices["right"]


def write_bool_matrix(file_name: str, matrix: TListMatrix):
    with open(file_name, "w") as file:
        json.dump(matrix, file)
