# Import Dependencies
import functools
from Flask import Blueprint, flash, g, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# Create Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')
