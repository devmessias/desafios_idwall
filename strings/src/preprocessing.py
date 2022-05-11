import re


def remove_multiple_spaces(string):
    """
    Remove multiple spaces
    """
    string = re.sub("\s\s+", " ", string)
    return string


def remove_tabs(string):
    """
    Remove tabs
    """
    string = re.sub("\t", "", string)
    return string


def replace_break_line(string):
    """
    Replace break line
    """
    # replace \n\s\n by \d
    string = re.sub("\n\n", "@d", string)
    return string