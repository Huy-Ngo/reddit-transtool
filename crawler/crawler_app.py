from http import HTTPStatus
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from json import loads
from .api import crawl, id_from_url

bp = Blueprint('app', __name__, url_prefix='/app')


def traverse_and_copy(comment, translations):
    cmt = {
        'author': comment['author'],
        'points': comment['points'],
        'text': '',
        'replies': [],
        'id': comment['id']
    }
    for cmt_id in translations:
        if cmt_id == f'trans-{cmt["id"]}':
            cmt['text'] = translations[cmt_id]
            break
    if comment['replies']:
        for reply in comment['replies']:
            rep = traverse_and_copy(reply, translations)
            cmt['replies'].append(rep)
    return cmt


def translate_thread(original, translations):
    """This takes the original comment thread and translations
    then output the translated comment thread
    """
    translated_thread = []
    for comment in original:
        translated_thread.append(traverse_and_copy(comment, translations))
    return translated_thread


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_id = request.form['post-id']
        url = request.form['url']
        if post_id == '':
            post_id = id_from_url(url)
        return redirect(url_for('app.translate', post_id=post_id))
    return render_template('app/home.html')


@bp.route('/<post_id>')
def translate(post_id):
    post = crawl(post_id)
    return render_template('app/translate.html', post=post)


@bp.route('/result/', methods=['POST'])
def result():
    s = request.args['post_id']
    post = crawl(s)
    comments = post['comments']
    translations = request.form
    return render_template(
        'app/result.html',
        comments=translate_thread(comments, translations),
        post=translations['post-trans'],
        original=post
    )
