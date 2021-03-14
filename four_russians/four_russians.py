import logging
import math
import typing as tp

from .bool_matrix import BoolMatrix
from .utils import bit_list_to_int


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _blocks_multiplication(
    left_block: BoolMatrix, right_block: BoolMatrix, block_size: int, dim_size: int
) -> BoolMatrix:
    """Helper for blocks multiplication

    Args:
        left_block (BoolMatrix): Column block [n x log(n)]
        right_block (BoolMatrix): Row block [log(n) x n]
        block_size (int): Reduced size of block (log(n))
        dim_size (int): Original size of matrices

    Returns:
        BoolMatrix: [description]
    """
    max_possible_size = 2 ** block_size
    possible_right_rows_sums = BoolMatrix(max_possible_size, dim_size)

    logger.debug(f"Number of possible right matrix's rows sums: {max_possible_size}")

    numbers_between_powers_of_two = 1
    block_row_index = 0

    for possible_sum_index in range(1, max_possible_size):
        possible_right_rows_sums[
            possible_sum_index
        ] = possible_right_rows_sums.sum_rows(
            possible_sum_index - 2 ** block_row_index,
            right_block,
            right_block.shape[0] - block_row_index - 1,
        )

        if numbers_between_powers_of_two == 1:
            numbers_between_powers_of_two = possible_sum_index + 1
            block_row_index += 1
        else:
            numbers_between_powers_of_two -= 1

    result = BoolMatrix(dim_size, dim_size)
    for row_index in range(dim_size):
        result[row_index] = possible_right_rows_sums[
            bit_list_to_int(left_block[row_index])
        ]

    return result


def multiply(left_matrix: BoolMatrix, right_matrix: BoolMatrix) -> BoolMatrix:
    """Four Russians algorithm for boolean multiplication of two matrices.
    Details:
    1. https://louridas.github.io/rwa/assignments/four-russians/
    2. https://link.springer.com/content/pdf/10.1007%2F978-0-387-88757-9_9.pdf

    Args:
        left_matrix (BoolMatrix): left-hand-side boolean matrix
        right_matrix (BoolMatrix): right-hand-side boolean matrix

    Returns:
        BoolMatrix: the result of boolean multiplication
    """
    assert (
        left_matrix.shape == right_matrix.shape
    ), "Left and right matrices should have equal shape"
    assert left_matrix.shape[0] == left_matrix.shape[1], "Matrices should be square"

    dim_size = left_matrix.shape[0]
    block_size = max(math.floor(math.log2(dim_size)), 1)
    number_of_blocks = math.ceil(dim_size / block_size)

    result = BoolMatrix(dim_size, dim_size)

    for block_index in range(number_of_blocks):
        left_block = left_matrix.get_column_block(block_index * block_size, block_size)
        right_block = right_matrix.get_row_block(block_index * block_size, block_size)
        block_multiplication_result = _blocks_multiplication(
            left_block, right_block, block_size, dim_size
        )
        result |= block_multiplication_result

    return result
