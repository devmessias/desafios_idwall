"""Module responsible for transforming the lxml elements and extracting useful information.
"""
from src.reddit.preprocessing import convert_numk2int


def extract_title(thread, params_bs):
    """Get the title and the url of the thread.

    Args:
        thread (lxml.etree.Element): The thread to extract the title from.
        params_bs (dict): The parameters for BeautifulSoup.
    Returns:
        (str, str): The title and the url of the thread.

    """
    title_el = thread.xpath(params_bs["xpath"]["title"])[0]
    title = title_el.text
    thread_link = title_el.get("href")
    return title, thread_link


def extract_comment_link(thread, params_bs):
    """Get the link to the comments of the thread.
    
    Args:
        thread (lxml.etree.Element): The thread to extract the title from.
        params_bs (dict): The parameters for BeautifulSoup.
    Returns:
        (str): The link to the comments of the thread.
    
    """
    comments = thread.xpath(params_bs["xpath"]["comments"])[0]
    comments_link = comments.get("href")
    return comments_link


def extract_score(thread, params_bs):
    """Get the score of the thread and check if it is valid.

    Args:
        thread (lxml.etree.Element): The thread to extract the title from.
        params_bs (dict): The parameters for BeautifulSoup.
    Returns:
        (int): The score of the thread.
        (bool): True if the score is not valid
    """

    score = thread.xpath(params_bs["xpath"]["score_unvoted"])[0].text
    score, discard = convert_numk2int(score)
    return score, discard