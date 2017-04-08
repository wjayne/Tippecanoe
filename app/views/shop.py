##Single tenant retail - General
import os
from xlrd import *
from flask import Blueprint, render_template
from flask import request
import pandas as pd

from functions import *
from app.settings import APP_STATIC

shop = Blueprint('shop', __name__)

def shop_output(parcel):

    hotels = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    if any(hotels.Parcel_ID == parcel):
        row = search_row(hotels, parcel)

        headers = row.dtypes.index

        title = get_title(row)
        info = get_golf_info(row)
        revenue = get_shop_revenue(row)
        expenses = get_shop_expenses(row)
        NOI = get_NOI(row)
        cap_rate = get_cap_rate(row)
        results = get_str_results(row)
        return render_template("output/shop.html", info=info,
                                                  revenue=revenue,
                                                  expenses=expenses,
                                                  NOI=NOI,
                                                  result=results,
                                                  title=title,
                                                  cap_rate=cap_rate)

    return "Parcel Number wasn't found"
