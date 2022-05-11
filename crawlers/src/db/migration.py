import argparse
import sqlite3


def create(local="reddit.db"):
    """Create a new database.

    Args:
        local (str): The path to the database.
    """
    con = sqlite3.connect(local)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS subreddits;")
    cur.execute('''
        CREATE TABLE subreddits(
            last_updated TIMESTAMP,
            subreddit VARCHAR(255),
            score INTEGER,
            title VARCHAR(255),
            thread_link TEXT,
            comment_link TEXT
        )
    ''')
    con.commit()
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true")
    args = parser.parse_args()
    if args.create:
        create()
