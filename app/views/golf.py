import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from functions import *
from app.settings import APP_STATIC

golf = Blueprint('golf', __name__)

@golf.route('/', methods=['POST'])
def golf_output():
    print "WE IN GOLF"
    parcel = request.form['parcelNumber']

    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    if any(hotels.Parcel_ID == parcel):
        row = search_row(hotels, parcel)
        #print_info(row)
        headers = row.dtypes.index
        #print row.dtypes
            #attributes
        info = get_golf_info(row)
        return render_template("output/golf.html", info=info)

    return "Parcel Number wasn't found"
