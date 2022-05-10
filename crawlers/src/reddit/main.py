import argparse
import multiprocessing as mp
from src.reddit.subreddit import main as subreddit_get


def invoke_subreddit(subreddit):
    """Multiprocsseing can't be used with a 
    generator, thus this function is used to invoke the subreddit_get
    
    """
    for _ in subreddit_get(subreddit):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subreddits", type=str, 
        help="Subreddits list separated by ;"
    )
    args = parser.parse_args()
    subreddits = args.subreddits.split(";")
    
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(invoke_subreddit, subreddits)