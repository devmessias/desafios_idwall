import argparse
import multiprocessing as mp
from src.reddit.subreddit import main as subreddit_get


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subreddits", type=str,
        help="Subreddits list separated by ;"
    )
    args = parser.parse_args()
    subreddits = args.subreddits.split(";")
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(subreddit_get, subreddits)