import argparse
import logging
import time
from bs4 import BeautifulSoup
from lxml import etree
from rich import print
import requests
import yaml

from src.reddit.preprocessing import check_sponsored
from src.reddit.transforms import extract_title, extract_comment_link, extract_score
from src.db.orm import SubredditDb


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def print_thread(subreddit, score, title, thread_link, comment_link):
    print(f"[bold blue]\t({subreddit})Score: {score}[/bold blue]|[green]{title}[/green]")
    print(f"\t[bold red]Thread: {thread_link}[bold /red]")
    print(f"\t[yellow]Comment: {comment_link}[/yellow]")


def get_subreddit_page_info(
        url, headers, params_bs, params_reddit, stdout=True, subreddit=""):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request to {url} failed with status code {response.status_code}")

    soup = BeautifulSoup(response.content, 'lxml')
    dom = etree.HTML(str(soup))
    reddit_threads = dom.xpath(params_bs["xpath"]["threads"])
    # reddit_threads = soup.find_all("div", class_=params_bs["class"]["threads"])
    # print votes, title
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
                "subreddit": subreddit,
                "title": title,
                "score": score,
                "thread_link": thread_link,
                "comment_link": comment_link
            }
        ]
        thread.clear()
        if stdout:
            print("\n")
            print_thread(
                subreddit, score, title, thread_link, comment_link)
    next_page_el = dom.xpath(params_bs["xpath"]["next_button"])
    if next_page_el:
        next_page_link = next_page_el[0].get("href")
        return data, next_page_link
    return data, None


def scrap_subreddit(params, subreddit_db, subreddit, stdout=True): 
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
        logger.debug(f"Scraping {next_page_link}")
        data, next_page_link = get_subreddit_page_info(
            next_page_link, headers, params_bs, params_reddit,
            subreddit=subreddit,
            stdout=stdout)
        subreddit_db.insert_threads(data)
        pages += 1
        yield data
        time.sleep(params_crawler["sleep_time_per_page"])
    return None


def main(subreddit, stdout=True):
    if stdout:
        print(f"[bold red] {subreddit.capitalize()} [/bold red]")
        print(f"[bold red] {'-'*len(subreddit)}[bold red]")
    with open("params.yaml", "r") as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    params_db = params["db"]
    cache_timeout = params_db["cache_timeout"]
    subreddit_db = SubredditDb()
    threads = subreddit_db.fetch_threads(subreddit)
    should_scrap = False
    if not threads:
        should_scrap = True
    else:
        last_updated = threads[0][0]
        should_scrap = int(time.time() - last_updated)/60 > cache_timeout
    if should_scrap:
        data = scrap_subreddit(params, subreddit_db, subreddit, stdout=stdout)
        for _ in data:
            yield data
    else:
        data = []
        for thread in threads:
            if stdout:
                print("\n")
                print_thread(
                    subreddit, thread[2], thread[3], thread[4], thread[5]
                )
            data += [
                {
                    "subreddit": subreddit,
                    "title": thread[3],
                    "score": thread[2],
                    "thread_link": thread[4],
                    "comment_link": thread[5]
                }
            ]
        yield data
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subreddit", help="Subreddit to scrape")
    parser.add_argument(
        "--stdout", action="store_false", help="Print to stdout", default=True)
    parser.add_argument(
        "--debug", action="store_true", help="set looger debug info", default=False)
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    for _ in main(args.subreddit, args.stdout):
        pass
