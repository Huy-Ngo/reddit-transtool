import praw
from flask import Flask
from json import load

app = Flask(__name__)


with open('secret.json', 'r') as f:
    data = load(f)
    client_id = data['client_ID']
    client_secret = data['client_secret']

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/Huy_Ngo)',
                     client_id=client_id, client_secret=client_secret)


def traverse(comment, n_tab):
    """
    This will use pre-order tree traversal for comment viewing,
    considering each comment is a tree
    :param comment: the top comment, i.e. the root of the tree
    :param n_tab: the level of indentation
    :return: None
    """
    cmt = {
        'author': comment.author.name,
        'points': comment.score,
        'text': comment.body,
        'replies': []
    }
    if comment.replies:
        for reply in comment.replies:
            cmt['replies'].append(traverse(reply, n_tab + 1))
    return cmt


@app.route('/<post_id>')
def index(post_id):
    submission = reddit.submission(id=post_id)
    post_info = {
        'title': submission.title,
        'text': submission.selftext,
        'author': submission.author.name,
        'subreddit': submission.subreddit.display_name,
        'points': submission.score,
        'id': submission.id,
        'n_comments': submission.num_comments,
        'comments': [],
    }
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    while comment_queue:
        cm = comment_queue.pop(0)
        post_info['comments'].append(traverse(cm, 0))
    return post_info
