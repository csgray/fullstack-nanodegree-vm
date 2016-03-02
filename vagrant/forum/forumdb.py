#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

"""
Original Python code that mimicks a database using a list
## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())
    DB.append((t, content))
"""


def GetAllPosts():
    """Get all posts from the database, sorted with the newest first."""
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    query = "SELECT content, time FROM posts ORDER BY time DESC"
    c.execute(query)
    rows = c.fetchall()
    posts = [{'content': str(bleach.clean(row[0])), 'time': str(row[1])} for row in rows]
    db.close()
    return posts


def AddPost(content):
    """Add a new post to the database.

    Args:
      content: The text content of the new post.
    """
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("INSERT INTO posts (content) VALUES (%s)",
              (content,))
    db.commit()
    db.close()
