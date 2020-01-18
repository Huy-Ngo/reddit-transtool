from http import HTTPStatus
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('app', __name__, url_prefix='/app')
