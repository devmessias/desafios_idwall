import sqlite3
import time


class SubredditDb:
    """A class to interact with the subreddits database."""
    def __init__(self, local="reddit.db"):
        """Initialize the class.
            Args:
                local (str): The path to the database.
        """
        self.local = local
        self.con = sqlite3.connect(f"file:{local}?mode=rw", uri=True)

    def fetch_threads(self, subreddit):
        """Filter the database for a subreddit
            Args:
                subreddit (str): The subreddit to filter for.
            Returns:
                list: A list of threads.
        """
        cur = self.con.cursor()
        cur.execute(
            "SELECT * FROM subreddits WHERE subreddit = ? ORDER BY last_updated DESC;", (subreddit,) )
        return cur.fetchall()

    def execute_insert(
            self, subreddit, score, title, 
            thread_link, comment_link, timestamp=None):
        """Execute a query.
            Args:
                subreddit (str): The subreddit the thread is in.
                score (int): The score of the thread.
                title (str): The title of the thread.
                thread_link (str): The link to the thread.
                comment_link (str): The link to the comments.
        """
        if timestamp is None:
            timestamp = time.time()
        self.cur.execute("INSERT INTO subreddits VALUES (?, ?, ?, ?, ?, ?)", (
            timestamp,
            subreddit,
            score,
            title,
            thread_link,
            comment_link
        ))

    def insert_thread(
            self, subreddit, score, title, thread_link, comment_link):
        """Insert a thread into the database.
            Args:
                subreddit (str): The subreddit the thread is in.
                score (int): The score of the thread.
                title (str): The title of the thread.
                thread_link (str): The link to the thread.
                comment_link (str): The link to the comments.
            Returns:
                int: last row id.
        """
        self.cur = self.con.cursor()
        self.execute_insert(
            subreddit, score, title, thread_link, comment_link)
        self.con.commit()
        return self.cur.lastrowid

    def insert_threads(self, threads):
        """Insert a list of threads into the database.
            Args:
                threads (list): A list of threads.
            Returns:
                int: last row id.
        """
        timestamp = time.time()
        self.cur = self.con.cursor()
        for thread in threads:
            self.execute_insert(
                timestamp=timestamp,
                **thread
            )
        self.con.commit()
        return self.cur.lastrowid

    def __del__(self):
        """Close the connection."""
        self.con.close()
