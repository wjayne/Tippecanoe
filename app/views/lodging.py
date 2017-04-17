import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd
import sys

from functions import *
from app.settings import APP_STATIC

lodging = Blueprint('lodging', __name__)

def lodging_output(parcel):
    print "YO"
    sys.stdout.flush()

    #with open(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx')) as f:
    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    if any(hotels.Parcel_ID == parcel):
        print "PRE - ANY"
        sys.stdout.flush()
        row = search_row(hotels, parcel)
        print "POST SEARCH ROW"
        sys.stdout.flush()
        #print_info(row)
        headers = row.dtypes.index
        #print row.dtypes
            #attributes
        info = get_info(row)
        revenue = get_revenue(row)
        expenses = get_expenses(row)
        NOI = get_NOI(row)
        cap_rate = get_cap_rate(row)
        result = get_results(row)
        children = get_child_parcels(row)
        return render_template("output/lodging.html", info=info
                                     , revenue=revenue
                                     , expenses=expenses
                                     , NOI=NOI
                                     , cap_rate=cap_rate
                                     , result=result
                                     , children=children)

    return "Parcel Number wasn't found"

def check_lodging():
    parcel = request.form['parcelNumber']
    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    row = search_row(hoels, parcel)
    print row["Category"].values
    checker = row['Category'].values
    if checker == 'Golf':
        pass
