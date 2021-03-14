import dataclasses
import pytest
import random
import numpy as np

from four_russians import BoolMatrix


@dataclasses.dataclass()
class MatrixParameters:
    height: int
    width: int

    def __str__(self) -> str:
        return f"Matrix of {self.height} x {self.width}"


MATRIX_PARAMETERS = [
    MatrixParameters(height=height, width=width)
    for height in range(1, 3, 5)
    for width in range(1, 3, 5)
]


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_default_creation(matrix_params: MatrixParameters):
    matrix = BoolMatrix(matrix_params.height, matrix_params.width, fill_value=True)
    raw_data = matrix.get_raw_data()

    assert matrix.shape == (matrix_params.height, matrix_params.width)
    assert len(raw_data) == matrix_params.height
    assert len(raw_data[0]) == matrix_params.width

    assert np.alltrue(np.asarray(raw_data))

    matrix = BoolMatrix(matrix_params.height, matrix_params.width, fill_value=False)
    raw_data = matrix.get_raw_data()

    assert matrix.shape == (matrix_params.height, matrix_params.width)
    assert len(raw_data) == matrix_params.height
    assert len(raw_data[0]) == matrix_params.width

    assert np.alltrue(np.asarray(raw_data) == False)


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_data_creation(matrix_params: MatrixParameters):
    np.random.seed(42)
    data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )

    matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=data.tolist()
    )
    raw_data = matrix.get_raw_data()

    assert matrix.shape == (matrix_params.height, matrix_params.width)
    assert len(raw_data) == matrix_params.height
    assert len(raw_data[0]) == matrix_params.width

    assert np.allclose(np.asarray(raw_data), data)


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_sum_rows(matrix_params: MatrixParameters):
    np.random.seed(42)
    random.seed(42)

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

    left_index = random.randint(0, matrix_params.height - 1)
    right_index = random.randint(0, matrix_params.height - 1)

    rows_sum = left_matrix.sum_rows(left_index, right_matrix, right_index)
    rows_sum = np.asarray(rows_sum)

    correct_sum = left_data[left_index] | right_data[right_index]

    assert np.allclose(rows_sum, correct_sum)


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_get_blocks(matrix_params: MatrixParameters):
    np.random.seed(42)
    random.seed(42)

    data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )

    matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=data.tolist()
    )

    row_start_index = random.randint(0, matrix_params.height - 1)
    row_block_size = random.randint(1, matrix_params.height - row_start_index)

    row_block = matrix.get_row_block(row_start_index, row_block_size)
    row_block_array = np.asarray(row_block.get_raw_data())

    assert row_block.shape == (row_block_size, matrix_params.width)
    assert np.allclose(
        row_block_array, data[row_start_index : row_start_index + row_block_size]
    )

    column_start_index = random.randint(0, matrix_params.width - 1)
    column_block_size = random.randint(1, matrix_params.width - column_start_index)

    column_block = matrix.get_column_block(column_start_index, column_block_size)
    column_block_array = np.asarray(column_block.get_raw_data())

    assert column_block.shape == (matrix_params.height, column_block_size)
    assert np.allclose(
        column_block_array,
        data[:, column_start_index : column_start_index + column_block_size],
    )


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_logical_or(matrix_params: MatrixParameters):
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

    or_matrix = left_matrix | right_matrix

    assert np.allclose(or_matrix.get_raw_data(), left_data | right_data)

    left_matrix |= right_matrix

    assert np.allclose(or_matrix.get_raw_data(), left_matrix.get_raw_data())


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_getitem(matrix_params: MatrixParameters):
    np.random.seed(42)

    data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )

    matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=data.tolist()
    )

    for i in range(matrix_params.height):
        assert np.allclose(data[i], matrix[i])

        for j in range(matrix_params.width):
            assert data[i, j] == matrix[i, j]


@pytest.mark.parametrize("matrix_params", MATRIX_PARAMETERS, ids=str)
def test_matrix_setitem(matrix_params: MatrixParameters):
    np.random.seed(42)

    data = np.random.randint(
        0, 2, size=(matrix_params.height, matrix_params.width), dtype=bool
    )

    matrix = BoolMatrix(
        matrix_params.height, matrix_params.width, fill_data=data.tolist()
    )

    for i in range(matrix_params.height):
        for j in range(matrix_params.width):
            matrix[i, j] = not matrix[i, j]

    assert np.allclose(matrix.get_raw_data(), ~data)
