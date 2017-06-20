import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd
import sys

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
from nonso import *
from app.settings import APP_STATIC

director = Blueprint('director', __name__)

# @director.route('/search',methods=['POST', 'GET'])
# def directions():
#     parcel = request.form['parcelNumber']
#     categoryTyper = get_type(parcel)
#     #categoryTyper = "Single Tenant Retail"
#     print categoryTyper
#     print "HERE I AM"
#     sys.stdout.flush()
#     if categoryTyper == 'Golf Course':
#         return golf_output()
#     elif categoryTyper == 'Lodging' or categoryTyper == 'Mobile Home Park':
#         return lodging_output()
#     elif categoryTyper == 'Single Tenant Retail':
#         return strg_output()
#     elif categoryTyper == 'Multi Tenant Retail':
#         return mtr_output()
#     elif categoryTyper == 'Self Storage':
#         return storage_output()
#     elif categoryTyper == 'Restaurant':
#         return rest_output()
#     elif categoryTyper.find('Office') != -1:
#         return office_output()
#     elif categoryTyper == 'Multi Family':
#         return mtf_output()
#     elif categoryTyper == 'Auto-Dealership':
#         return auto_output()
#     elif categoryTyper =='Shop/Utility' or categoryTyper == 'Auto-Garage' or 'Auto' in categoryTyper:
#         return shop_output()
#     elif categoryTyper.find('Manufacturing') != -1 or categoryTyper == 'Warehouse/Distribution':
#         return mfg_output(parcel)
#     else:
#         print "nonso"
#         return render_template("home/index.html", error="Parcel not found")

@director.route('/search/<string:parcelNumber>', methods=['GET'])
def search(parcelNumber):
    parcel = parcelNumber
    categoryTyper = get_type(parcel)
    #categoryTyper = "Single Tenant Retail"
    print categoryTyper
    #print "HERE I AM"
    sys.stdout.flush()
    if categoryTyper.find('Golf Course') != -1:
        return golf_output(parcel)
    elif categoryTyper.find('Lodging') != -1 or categoryTyper.find('Mobile Home Park') != -1:
        return lodging_output(parcel)
    elif categoryTyper.find('Single Tenant Retail') != -1:
        return strg_output(parcel)
    elif categoryTyper.find('Multi Tenant Retail') != -1:
        return mtr_output(parcel)
    elif categoryTyper.find('Self Storage') != -1:
        return storage_output(parcel)
    elif categoryTyper.find('Restaurant') != -1:
        return rest_output(parcel)
    elif categoryTyper.find('Office') != -1:
        return office_output(parcel)
    elif categoryTyper.find('Multi-Family') != -1:
        return mtf_output(parcel)
    elif categoryTyper.find('Auto-Dealership') != -1:
        return auto_output(parcel)
    elif categoryTyper.find('Shop/Utility') != -1 or categoryTyper.find('Auto-Garage') != -1 or 'Auto' in categoryTyper:
        return shop_output(parcel)
    elif categoryTyper.find('Manufacturing') != -1 or categoryTyper == 'Warehouse/Distribution':
        return mfg_output(parcel)
    else:
        print "Type not found"
	print categoryTyper
        return render_template("home/index.html", error="Parcel not found")

