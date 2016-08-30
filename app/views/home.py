from flask import Blueprint, render_template
from flask import request

home = Blueprint('index', __name__)

@home.route('/')
def index():
    return render_template('home/index.html')
