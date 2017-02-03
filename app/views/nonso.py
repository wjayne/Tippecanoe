import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from functions import *
from app.settings import APP_STATIC

nonso = Blueprint('nonso', __name__)

@nonso.route('/', methods=['POST', 'GET'])
def nonso_output():
    #print "---" + thingy
    # parcel = request.form['parcelNumber']

    # #with open(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx')) as f:
    # hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    # if any(hotels.Parcel_ID == parcel):
    #     row = search_row(hotels, parcel)
    #     #print_info(row)
    #     headers = row.dtypes.index
    #     #print row.dtypes
    #         #attributes
    #     info = get_info(row)
    #     revenue = get_revenue(row)
    #     expenses = get_expenses(row)
    #     NOI = get_NOI(row)
    #     cap_rate = get_cap_rate(row)
    #     result = get_results(row)
        return render_template("home/index.html")

def check_lodging():
    parcel = request.form['parcelNumber']
    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    row = search_row(hoels, parcel)
    print row["Category"].values
    checker = row['Category'].values
    if checker == 'Golf':
        pass
