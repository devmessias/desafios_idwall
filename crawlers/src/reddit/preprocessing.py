def convert_number_k_format_to_number(number_k_format):
    """
    Converts a number in K format to a number.
    :param number_k_format:
    :return:
    """
    decomp = number_k_format.split('k')
    if len(decomp) == 0:
        return 0
    if len(decomp) == 1:
        if not decomp[0].isdigit():
            raise ValueError(f"{number_k_format} is not a valid number")
        return int(decomp[0])
    # pop the fist element of the list
    number = float(decomp.pop(0))
    if not all([len(x) == 0 for x in decomp]):
        raise ValueError(f"{number_k_format} is not a valid number")

    return int(number*(1000)**len(decomp))