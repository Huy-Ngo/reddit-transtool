from http import HTTPStatus
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .api import crawl, crawl_by_url

bp = Blueprint('app', __name__, url_prefix='/app')


@bp.route('/')
def index():
    return render_template('app/home.html')


@bp.route('/<post_id>')
def result(post_id):
    post = crawl(post_id)
    return render_template('app/translate.html', post=post)


@bp.route('/submit/', methods=['POST'])
def submit():
    return request.form['meta-trans']
