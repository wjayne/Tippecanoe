##Single tenant retail - General
import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from functions import *
from app.settings import APP_STATIC

office = Blueprint('office', __name__)

def office_output(parcel):

    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    if any(hotels.Parcel_ID == parcel):
        row = search_row(hotels, parcel)

        headers = row.dtypes.index

        info = get_golf_info(row)# works
        revenue = get_str_revenue(row)
        expenses = get_office_expenses(row)#Need to make
        NOI = get_NOI(row)
        cap_rate = get_cap_rate(row)
        results = get_str_results(row)
        return render_template("output/office.html", info=info,
                                                  revenue=revenue,
                                                  expenses=expenses,
                                                  NOI=NOI,
                                                  result=results,
                                                  cap_rate=cap_rate)

    return "Parcel Number wasn't found"
