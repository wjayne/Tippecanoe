import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from functions import *
from app.settings import APP_STATIC

lodging = Blueprint('lodging', __name__)

def lodging_output(parcel):

    #with open(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx')) as f:
    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    if any(hotels.Parcel_ID == parcel):
        row = search_row(hotels, parcel)
        print "B"
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
        return render_template("output/lodging.html", info=info
                                     , revenue=revenue
                                     , expenses=expenses
                                     , NOI=NOI
                                     , cap_rate=cap_rate
                                     , result=result)

    return "Parcel Number wasn't found"

def check_lodging():
    parcel = request.form['parcelNumber']
    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    row = search_row(hoels, parcel)
    print row["Category"].values
    checker = row['Category'].values
    if checker == 'Golf':
        pass
