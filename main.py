import click
import logging

import four_russians as fr
import utils


logger = logging.getLogger(__name__)
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger.setLevel(logging.DEBUG)


@click.command()
@click.argument(
    "data_read_path", type=click.Path(file_okay=True, readable=True, resolve_path=True)
)
@click.option(
    "result_write_path",
    "--result_write_path",
    default=None,
    type=click.Path(file_okay=True, writable=True, resolve_path=True),
)
def main(data_read_path: str, result_write_path: str = None):
    logger.debug("Reading data")
    left_matrix_data, right_matrix_data = utils.read_bool_matrices(data_read_path)

    dim_size = len(left_matrix_data)

    logger.debug("Creating `BoolMatrix` objects")
    left_matrix = fr.BoolMatrix(dim_size, dim_size, fill_data=left_matrix_data)
    right_matrix = fr.BoolMatrix(dim_size, dim_size, fill_data=right_matrix_data)

    logger.debug("Computing results")
    result_matrix = fr.multiply(left_matrix, right_matrix)
    result = result_matrix.get_raw_data()

    if result_write_path:
        utils.write_bool_matrix(result_write_path, result)
    else:
        logger.info(f"Multiplication result is {result}")


if __name__ == "__main__":
    main()
