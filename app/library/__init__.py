from flask import Blueprint

library_mod = Blueprint('library_mod', __name__)

from . import views
