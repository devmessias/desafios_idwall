import argparse
import time
from bs4 import BeautifulSoup
from lxml import etree
from rich import print
import requests
import yaml

from src.reddit.preprocessing import convert_numk2int, check_sponsored


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


def get_subreddit_page_info(
        url, headers, params_bs, params_reddit, stdout=True):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request to {url} failed with status code {response.status_code}")

    soup = BeautifulSoup(response.content, 'lxml')
    dom = etree.HTML(str(soup))
    reddit_threads = dom.xpath(params_bs["xpath"]["threads"])
    # reddit_threads = soup.find_all("div", class_=params_bs["class"]["threads"])
    # print votes, title
    if stdout:
        print(f"[bold green] {len(reddit_threads)} threads found [/bold green]")
        print("\n")
        print(f"[blue]Vote{' '*5}[/blue]|[green]Title{' '*80}[/green]")
        print("-"*len(f"Vote{' '*5}| Title{' '*80}"))
    data = []
    for thread in reddit_threads:
        sponsored = check_sponsored(thread)
        if sponsored:
            thread.clear()
            continue
        score, discard = extract_score(thread, params_bs)
        if discard:
            thread.clear()
            continue
        if score < params_reddit["min_score"]:
            thread.clear()
            continue
        title, thread_link = extract_title(thread, params_bs)
        comment_link = extract_comment_link(thread, params_bs)
        data += [
            {
                "title": title,
                "score": score,
                "thread_link": thread_link,
                "comment_link": comment_link
            }
        ]
        thread.clear()
        if stdout:
            print(f"[bold blue]{score:<9}[/bold blue]|[green]{title:<50}[/green]")
    next_page_el = dom.xpath(params_bs["xpath"]["next_button"])
    if next_page_el:
        next_page_link = next_page_el[0].get("href")
        return data, next_page_link
    return data, None


def main(subreddit):
    print(f"[bold red] {subreddit.capitalize()} [/bold red]")
    print(f"[bold red] {'-'*len(subreddit)}[bold red]")
    with open("params.yaml", "r") as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    params_crawler = params["crawler"]
    params_bs = params["beautiful_soup"]
    params_reddit = params["reddit"]

    headers = params_bs["headers"]
    base_url = f"{params_reddit['base_url']}/r/{subreddit}/"
    query_params = f"sort=top&t={params_reddit['links_from']}"
    url = f"{base_url}?{query_params}"
    next_page_link = url
    pages = 0
    while next_page_link and pages < params_crawler["max_paginations"]:
        data, next_page_link = get_subreddit_page_info(
            next_page_link, headers, params_bs, params_reddit)
        pages += 1
        time.sleep(params_crawler["sleep_time_per_page"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subreddit", help="Subreddit to scrape")
    args = parser.parse_args()
    main(args.subreddit)
