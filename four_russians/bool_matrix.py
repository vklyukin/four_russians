import typing as tp
from copy import deepcopy


TListMatrix = tp.List[tp.List[bool]]


class BoolMatrix:
    """Wrapper for boolean matrices. Used in four russians algorithm for bit multiplication"""

    def __init__(
        self,
        height: int,
        width: int,
        fill_value: bool = False,
        fill_data: tp.Optional[TListMatrix] = None,
    ):
        """Constructor

        Args:
            height (int): number of rows
            width (int): number of columns
            fill_value (bool, optional): default value for matrix. Defaults to False.
            fill_data (TListMatrix, optional): overwrites matrix's data if given. Defaults to None.
        """
        assert isinstance(fill_value, bool), "`fill_value` should be of type `bool`"
        assert (
            height > 0 and width > 0
        ), "`height` and 'width` parameters should be positive"

        self._height = height
        self._width = width

        if fill_data is None:
            self._data = [[fill_value for _ in range(width)] for _ in range(height)]
        else:
            self._height = min(self._height, len(fill_data))
            self._width = min(self._width, len(fill_data[0]))
            self._data = deepcopy(fill_data)

    @property
    def shape(self) -> tp.Union[int, int]:
        return self._height, self._width

    def sum_rows(
        self, self_index: int, other: "BoolMatrix", other_index: int
    ) -> tp.List[int]:
        """Logical OR of rows of two matrices according to the given indices.

        Args:
            self_index (int): row index of matrix-caller
            other (BoolMatrix): rhs matrix
            other_index (int): rhs matrix's row index

        Returns:
            tp.List[int]: the result of logical OR
        """
        row = self._data[self_index].copy()
        for index, other_element in enumerate(other[other_index]):
            row[index] |= other_element
        return row

    def get_row_block(self, start_index: int, block_size: int) -> "BoolMatrix":
        """Create block of rows extracted from the original matrix

        Args:
            start_index (int): start row index
            block_size (int): block size

        Returns:
            BoolMatrix: extracted block
        """
        assert (
            start_index < self._height
        ), "`start_index` should be less than matrix height"
        real_block_size = min(block_size, self._height)

        block_data = self._data[start_index : start_index + real_block_size]
        block = BoolMatrix(real_block_size, self._width, fill_data=block_data)

        return block

    def get_column_block(self, start_index: int, block_size: int) -> "BoolMatrix":
        """Create block of columns extracted from the original matrix

        Args:
            start_index (int): start column index
            block_size (int): block size

        Returns:
            BoolMatrix: extracted block
        """
        assert (
            start_index < self._width
        ), "`start_index` should be less than matrix width"
        real_block_size = min(block_size, self._width)

        block_data = [
            self._data[i][start_index : start_index + real_block_size]
            for i in range(self._height)
        ]
        block = BoolMatrix(self._height, real_block_size, fill_data=block_data)

        return block

    def get_raw_data(self) -> TListMatrix:
        """Outputs copy of the matrix data

        Returns:
            tp.List[tp.List[bool]]: Matrix data
        """
        return deepcopy(self._data)

    def __getitem__(self, index: tp.Union[int, tp.Tuple[int, int]]) -> bool:
        if isinstance(index, int):
            return self._data[index]
        elif isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self._data[i][j]
        else:
            raise RuntimeError("Wrong format of index: should be int or 2-length tuple")

    def __setitem__(self, index: tp.Union[int, tp.Tuple[int, int]], value: bool):
        if isinstance(index, int):
            self._data[index] = value
        elif isinstance(index, tuple) and len(index) == 2:
            i, j = index
            self._data[i][j] = value
        else:
            raise RuntimeError("Wrong format of index: should be int or 2-length tuple")

    def __or__(self, other: "BoolMatrix") -> "BoolMatrix":
        new_bool_matrix = BoolMatrix(self._height, self._width)
        for height_index in range(self._height):
            for width_index in range(self._width):
                new_bool_matrix[height_index, width_index] = (
                    self._data[height_index][width_index]
                    | other[height_index, width_index]
                )
        return new_bool_matrix

    def __ior__(self, other: "BoolMatrix"):
        for height_index in range(self._height):
            for width_index in range(self._width):
                self._data[height_index][width_index] |= other[
                    height_index, width_index
                ]
        return self
