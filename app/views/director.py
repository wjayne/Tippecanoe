import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from rest import *
from office import *
from storage import *
from lodging import *
from golf import *
from strg import *
from mtr import *
from multi_family import *
from functions import *
from shop import *
from auto import *
from mfg import *
from app.settings import APP_STATIC

director = Blueprint('director', __name__)

@director.route('/',methods=['POST', 'GET'])
def directions():
    parcel = request.form['parcelNumber']
    categoryTyper = get_type(parcel)
    #categoryTyper = "Single Tenant Retail"
    print categoryTyper
    if categoryTyper == 'Golf Course':
        return golf_output()
    elif categoryTyper == 'Lodging':
        return lodging_output()
    elif categoryTyper == 'Single Tenant Retail':
        return strg_output()
    elif categoryTyper == 'Multi Tenant Retail':
        return mtr_output()
    elif categoryTyper == 'Self Storage':
        return storage_output()
    elif categoryTyper == 'Restaurant':
        return rest_output()
    elif categoryTyper.find('Office') != -1:
        return office_output()
    elif categoryTyper == 'Multi-Family':
        return mtf_output()
    elif categoryTyper =='Shop/Utility' or categoryTyper == 'Auto-Garage':
        return shop_output()
    elif categoryTyper == 'Auto-Dealership':
        return auto_output()
    elif categoryTyper.find('Manufacturing') != -1 or categoryTyper == 'Warehouse/Distribution':
        return mfg_output()
    else:
        print "nonso"
