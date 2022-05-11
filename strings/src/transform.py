
import re


def apply_justify(line, char_limit):
    """Jusify a line given a character limit

    Args:
        line (str): line to justify
        char_limit (int): character limit
    Returns:
        str: justified line
    """

    justified = ""
    words = line.split()
    missing_spaces = char_limit - sum([len(word) for word in words])
    while missing_spaces > 0 and len(words) > 1:
        for i in range(len(words) - 1):
            words[i] += " "
            missing_spaces -= 1
            if missing_spaces < 1:
                break

    justified = "".join(words)

    return justified


def greedy_wrap(txt, char_limit=40, justify=False):
    """Word wrap solution using greedy algorithm.

    Args:
        txt (str): Text to wrap.
        char_limit (int): Character limit.
        justify (bool): Justify text.
    Returns:
        str: Wrapped text.
    """
    line = ""
    wrap_text = ""
    list_elem = re.split("(\s|\n|@d)", txt)
    n_elem = len(list_elem)
    for i, word in enumerate(list_elem):
        if word == "@d":
            if justify:
                line = apply_justify(line, char_limit)
            wrap_text += line + "\n\n"
            line = ""
            continue

        if word in (" ", "\n"):
            continue
        if line == "":
            line = word
        elif len(line) + len(word) + 1 <= char_limit:
            line += " " + word
            if i == n_elem - 1 and justify:
                line = apply_justify(line, char_limit)
        else:
            if justify:
                line = apply_justify(line, char_limit)
            wrap_text += line + "\n"
            line = word

    wrap_text += line

    return wrap_text