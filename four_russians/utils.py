import typing as tp


def bit_list_to_int(bit_list: tp.List[bool]) -> int:
    result = 0
    number_of_bits = len(bit_list)

    for power, bit in enumerate(bit_list):
        if bit:
            result += 2 ** (number_of_bits - power - 1)

    return result
