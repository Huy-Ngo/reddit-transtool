from http import HTTPStatus
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from wtforms import TextAreaField
from .api import crawl, id_from_url

bp = Blueprint('app', __name__, url_prefix='/app')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_id = request.form['post-id']
        url = request.form['url']
        if post_id == '':
            post_id = id_from_url(url)
        return redirect(url_for('app.result', post_id=post_id))
    return render_template('app/home.html')


@bp.route('/<post_id>')
def result(post_id):
    post = crawl(post_id)
    return render_template('app/translate.html', post=post)


@bp.route('/submit/', methods=['POST'])
def submit():
    return request.form
