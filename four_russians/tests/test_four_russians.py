import dataclasses
import pytest
import random
import numpy as np

from four_russians import BoolMatrix, multiply


@dataclasses.dataclass()
class MatrixParameters:
    height: int
    width: int

    def __str__(self) -> str:
        return f"Matrix of {self.height} x {self.width}"


MATRIX_PARAMETERS = [
    MatrixParameters(height=dim_size, width=dim_size)
    for dim_size in (1, 3, 5, 20, 50, 100, 200, 400, 700)
]


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_four_russians_multiplication(matrix_params: MatrixParameters):
    np.random.seed(42)

    left_data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )
    right_data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )

    left_matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=left_data.tolist()
    )
    right_matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=right_data.tolist()
    )

    four_russians_result = multiply(left_matrix, right_matrix)
    np_result = left_data @ right_data

    assert np.allclose(four_russians_result.get_raw_data(), np_result)
