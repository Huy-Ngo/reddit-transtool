import praw
from json import load


with open('secret.json', 'r') as f:
    data = load(f)
    client_id = data['client_id']
    client_secret = data['client_secret']

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/Huy_Ngo)',
                     client_id=client_id, client_secret=client_secret)

submission = reddit.submission(id='ejc2ns')


def print_block(text, n_tab):
    text = text.replace('\n\n', '\n' + '\t' * n_tab)
    print('\t'*n_tab, end='')
    print(text)


def traverse(comment, n_tab):
    """
    This will use pre-order tree traversal for comment viewing,
    considering each comment is a tree
    :param comment: the top comment, i.e. the root of the tree
    :param n_tab: the level of indentation
    :return: None
    """
    print_block(comment.body, n_tab)
    if comment.replies:
        for reply in comment.replies:
            traverse(reply, n_tab + 1)
            print('')


submission.comments.replace_more(limit=None)
comment_queue = submission.comments[:]  # Seed with top-level
while comment_queue:
    cm = comment_queue.pop(0)
    traverse(cm, 0)
    print('-----')
