"""Module  responsible for dealing with the text extraction and storage."""


def load_from_file(file_path):
    """Loads a file to a string."""
    with open(file_path, "r") as file:
        txt = file.read()
    return txt


def save_to_file(file_path, txt):
    """Saves a string to a file."""
    with open(file_path, "w") as file:
        file.write(txt)
