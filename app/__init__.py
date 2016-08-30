from flask import Flask, render_template
from views import functions
import os

app = Flask(__name__)

#JANK ASS 2 DANK HAMMER
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Import Blueprints
from .views.home import home
from .views.lodging import lodging
from .views.golf import golf
from .views.director import director
from .views.strg import strg
from .views.mtr import mtr
from .views.storage import storage
from .views.rest import rest
from .views.office import office
from .views.multi_family import mtf
from .views.shop import shop
from .views.auto import auto
from .views.mfg import mfg

app.register_blueprint(home)
app.register_blueprint(director)#, url_prefix='/ayy')
app.register_blueprint(lodging)
app.register_blueprint(golf)
app.register_blueprint(strg)
app.register_blueprint(mtr)
app.register_blueprint(storage)
app.register_blueprint(rest)
app.register_blueprint(office)
app.register_blueprint(mtf)
app.register_blueprint(shop)
app.register_blueprint(auto)
app.register_blueprint(mfg)
