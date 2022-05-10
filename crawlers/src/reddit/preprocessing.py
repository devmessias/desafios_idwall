def convert_numk2int(number_k_format):
    """
    Converts a number in K format to a number.
    :param number_k_format:
    :return:
    """
    if number_k_format == "•":
        return 0, True

    decomp = number_k_format.split('k')
    if len(decomp) == 0:
        raise ValueError(f"Invalid number format: {number_k_format}")
    if len(decomp) == 1:
        if not decomp[0].isdigit():
            raise ValueError(f"{number_k_format} is not a valid number")
        return int(decomp[0]), False
    # pop the fist element of the list
    number = float(decomp.pop(0))
    if not all([len(x) == 0 for x in decomp]):
        raise ValueError(f"{number_k_format} is not a valid number")

    return int(number*(1000)**len(decomp)), False


def check_sponsored(thread):
    """
    Checks if the thread is sponsored.

    Args:
        thread (lxml.etree.Element): The thread to extract the title from.
        params_bs (dict): The parameters for BeautifulSoup.
    Returns:
        (bool): True if the thread is sponsored.
    """
    classes = thread.get("class")
    sponsored = "promoted" in classes
    return sponsored
  