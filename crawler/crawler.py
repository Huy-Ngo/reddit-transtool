import praw
from json import load
from http import HTTPStatus

# eo8zee

with open('./crawler/secret/secret.json', 'r') as f:
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


def crawl(post_id=None, url=None):
    if post_id is not None:
        submission = reddit.submission(id=post_id)
    elif url is not None:
        submission = reddit.submission(url=url)
    else:
        return {
            'status': HTTPStatus.BAD_REQUEST,
            'message': 'Bad Request',
            'details': 'No url or post id inserted'
        }
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
