import os
import numpy as np
import pandas as pd
import openpyxl
from math import floor
from app.settings import APP_STATIC
import locale
import sys
#class to passs
global excelData
locale.setlocale(locale.LC_ALL, '')
class tuple:
    column = ""
    value = ""

    def __init__(self, column, name):
        self.column = column
        self.value = name

#function to read in excel files as dataframes
#returns the first first sheet as an object
def read_excel(file):
    global excelData
    try:
        print "SAVE TIME"
        sys.stdout.flush()
        return excelData
    except:
        xl = openpyxl.load_workbook(file)
        sheet = xl.get_sheet_by_name('Sheet1')
        sheetpass = pd.DataFrame()
        sheetpass = pd.read_excel(file)
        excelData = sheetpass
        return sheetpass
    # if excelData == None:
    #     xl = openpyxl.load_workbook(file)
    #     sheet = xl.get_sheet_by_name('Query1')
    #     sheetpass = pd.DataFrame()
    #     sheetpass = pd.read_excel(file)
    #     excelData = sheetpass
    #     return sheetpass
    # else:
    #     return excelData

#functino to search the row corresponding to the input parcel
def search_row(df, parcel):
    print "ROW SEARHC"
    sys.stdout.flush()
    return df.loc[df['Parcel_ID'] == parcel]

#prints out in format
def print_info(row):
    print "*********************"
    print "*Basic Property Info*"
    print "*********************"
    print "Major Property Type:", row['Category'].values
    print "Sub Type:", row['Sub_Category'].values
    print "DBA:", row['DBA'].values
    word = str(row['DBA'].values) # print "DBA:",
    print "Address:", row['Address'].values, row['City'].values, row['ZIP'].values
    print "Year Built:", row['Year Built'].values
    print "Amenities:", row['Amenities (5=best 1=worst)'].values
    print "Appeal:", row['Appeal (5=best 1=worst)'].values
    print "Franchise:", row['Franchise'].values
    print "-----TEST-----"
    start = word.index('\'')+1
    end = len(word) - 2
    print word[start:end]

    #print "Rent Class:", row['Rent Class(5=best 1=worst)']

def get_info(row):
    #print "HERESUIDDIUENEIUNOEIUFHIUENH"
    info = []
    info2 = []
    info.append(row['Category'])
    info.append(row['Sub_Category'])
    info.append(row['DBA'])
    info.append(row['Address'])
    info.append(row['City'])
    info.append(row['ZIP'])
    info.append(row['Year_Built'])
    info.append(row['Amenities (5=best 1=worst)'])
    # info.append(row['Appeal (5=best 1=worst)'])
    info.append(row['Franchise'])
    for word in info:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
        if 'nan' not in k.value:
            info2.append(k)
        else:
            k.value = 'MISSING'
            info2.append(k)

    return info2

def get_revenue(row):
    #it will give KeyError if not found
    revenue = []
    revenue2 = []
    revenue.append(row['Rooms'])
    revenue.append(row['Lodging_Rate'])
    #revenue.append(row['Projected Actual Rate'])
    #revenue.append(row['Projected Actual Suite Rate'])
    #revenue.append(row['Prime Rate 28 Days per Year'])
    #revenue.append(row['Weighted Rate'])
    revenue.append(row['Additional Income'])
    revenue.append(row['PGI'])
    revenue.append(row['Occupancy'])
    revenue.append(row['EGI'])
    #CLEANING UP EDIT:WILL
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        elif k.column != 'Suites' and k.column != 'Rooms':
            k.value = locale.currency(float(k.value), grouping=True)
        revenue2.append(k)
    return revenue2

def get_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Lodging_Dept_Exp'])
    expenses.append(row['Lodging_Franchise_Fee'])
    expenses.append(row['Lodging_Insurance'])
    expenses.append(row['Lodging_Undist_Exp'])
    expenses.append(row['Lodging_Management'])
    expenses.append(row['Lodging_ReplaceReserve'])
    expenses.append(row['Total_Expenses (%EGI)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if 'nan' not in k.value:
            k.value = str(to_percent(float(k.value), 2))
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)

    return expenses2

def get_NOI(row):
    item = row['NOI'].round(decimals=2)
    word = str(item.values)
    word = word[1:len(word)-1]
    if word != 'nan' and word != ' nan' and 'nan' not in word:
        return locale.currency(float(word), grouping=True)
    return "To be calcualted"

def get_cap_rate(row):
    cap_rate = []
    cap_rate2 = []
    cap_rate.append(row['Cap Rate'])
    cap_rate.append(row['Tax Rate'])
    cap_rate.append(row['Loaded Rate'])
    for word in cap_rate:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = str(to_percent(float(k.value), 2))
            cap_rate2.append(k)
        else:
            k.value = 'MISSING'
            cap_rate2.append(k)

    return cap_rate2

def get_results(row):
    result = []
    result2 = []
    result.append(row['TotalWorkbookValue'])
    result.append(row['Pers_Prop'])
    result.append(row['RE_TTV'])
    result.append(row['AV/Unit'])
    result.append(row['Notes'])
    for word in result:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value
        if k.value != "nan" and k.value != ' nan' and 'nan' not in k.value:
            if k.column != 'Notes':
                k.value = locale.currency(float(k.value), grouping=True)
            result2.append(k)
        else:
            k.value = 'MISSING'
            result2.append(k)
    return result2

def to_percent(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

def get_type(parcelnumber):
    print "BEFOR XCEL"
    #sys.stdout.flush()
    table1 = read_excel(os.path.join(APP_STATIC, 'Copy of MASTER INCOME DATA.xlsx'))
    print "AFTER XCEL"
    sys.stdout.flush()
    row1 = search_row(table1, parcelnumber)
    u =  str(row1['Category'].values)
    start = u.find('\'')+1
    end = len(u) - 2
    u = u[start:end]
    return u

## also works for single tenant retail
def get_golf_info(row):
    info = []
    info2 = []
    info.append(row['Category'])
    info.append(row['Sub_Category'])
    info.append(row['DBA'])
    info.append(row['Address'])
    info.append(row['City'])
    info.append(row['ZIP'])
    info.append(row['Year_Built'])
    info.append(row['Appeal (5=best 1=worst)'])
    #CLEANING UP EDIT:WILL
    for word in info:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])

        if 'nan' not in k.value or len(k.value) > 5:
            info2.append(k)
        else:
            k.value = 'MISSING'
            info2.append(k)
    return info2

def get_str_revenue(row):
    revenue = []
    revenue2 = []
    revenue.append(row['Square_Feet'])
    revenue.append(row['Unused_SF'])
    revenue.append(row['Retail_Rent'])
    revenue.append(row['PGI'])
    revenue.append(row['Vacancy'])
    revenue.append(row['PGI'])
    revenue.append(row['EGI'])
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        print "K VALUE vvvvvvvvv"
        print k.value
        sys.stdout.flush()
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        if k.value != ' nan' and k.value != 'nan' and 'nan' not in k.value:
            k.value = locale.currency(float(k.value), grouping=True)
            revenue2.append(k)
        else:
            k.value = 'MISSING'
            revenue2.append(k)
    return revenue2

def get_str_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Retail_Mgmt'])
    expenses.append(row['Retail_Insurance'])
    expenses.append(row['Retail_Maint'])
    expenses.append(row['Retail_Replacements'])
    expenses.append(row['Total_Exp ($/SF)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = locale.currency(float(k.value), 2)
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)
    return expenses2

def get_str_results(row):
    result = []
    result2 = []
    result.append(row['TotalWorkbookValue'])
    result.append(row['Pers_Prop'])
    result.append(row['RE_TTV'])
    result.append(row['AV/SF'])
    result.append(row['Notes'])
    for word in result:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if "$" not in k.value:
            try:
                k.value = locale.currency(float(k.value), grouping=True)
            except ValueError:
                k.value = k.value;
        if 'nan' not in k.value:        
            result2.append(k)
        else:
            k.value = 'MISSING'
            result2.append(k)
    return result2

def mtr_center_revenue(row):
    #print "here"
    revenue = []
    revenue2 = []
    revenue.append(row['Square_Feet'])
    revenue.append(row['Anchor_1_SF'])
    revenue.append(row['Anchor_2_SF'])
    revenue.append(row['Anchor_3_SF'])
    revenue.append(row['In_Line_SF'])
    revenue.append(row['Unused_SF'])
    revenue.append(row['Retail_Rent'])
    revenue.append(row['PGI'])
    revenue.append(row['Vacancy'])
    revenue.append(row['EGI'])
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        elif k.column != 'Suites' and k.column != 'Rooms':
            k.value = "$" + k.value
        if 'nan' not in k.value:
            revenue2.append(k)
        else:
            k.value = 'MISSING'
            revenue.append(k)
    return revenue2

def get_storage_revenue(row):
    revenue = []
    revenue2 = []
    revenue.append(row['Square_Feet'])
    revenue.append(row['Storage Rent'])
    revenue.append(row['PGI'])
    revenue.append(row['Vacancy'])
    revenue.append(row['PGI'])
    revenue.append(row['EGI'])
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        elif k.column != 'Suites' and k.column != 'Rooms':
            locale.currency(float(k.value), grouping=True)
        if 'nan' not in k.value:
            revenue2.append(k)
        else:
            k.value = 'MISSING'
            revenue2.append(k)
        return revenue2

def get_storage_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Storage Admin'])
    expenses.append(row['Storage Undist'])
    expenses.append(row['Storage Insurance'])
    expenses.append(row['Storage Maint'])
    expenses.append(row['Storage Mgmt'])
    expenses.append(row['Storage Utilities'])
    expenses.append(row['Storage RepRes'])
    expenses.append(row['Total_Exp ($/SF)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = locale.currency(float(k.value), grouping=True)
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)
    return expenses2

def get_office_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Office_Mgmt'])
    expenses.append(row['Office_Admin'])
    expenses.append(row['Office_Insurance'])
    expenses.append(row['Office_Maint'])
    expenses.append(row['Office_Replacements'])
    expenses.append(row['Total_Exp ($/SF)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = locale.currency(float(k.value), grouping=True)
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)
    return expenses2


def get_multi_family_revenue(row):
    revenue = []
    revenue2 = []
    revenue.append(row['Units'])
    revenue.append(row['Unit_Rent'])
    revenue.append(row['Vacancy'])
    revenue.append(row['Additional Income'])
    revenue.append(row['PGI'])
    revenue.append(row['EGI'])
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        elif k.column != 'Suites' and k.column != 'Rooms':
            k.value = locale.currency(float(k.value), grouping=True)
        if 'nan' not in k.value:
            revenue2.append(k)
        else:
            k.value = 'MISSING'
            revenue2.append(k)
        return revenue2

def get_mf_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Apt_Mgmt'])
    expenses.append(row['Apt_Insurance'])
    expenses.append(row['Apt_Maint'])
    expenses.append(row['Apt_Utilities'])
    expenses.append(row['Apt_Replacements'])
    expenses.append(row['Total_Expenses (%EGI)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = locale.currency(float(k.value), grouping=True)
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)
    return expenses2

def get_mf_results(row):
    result = []
    result2 = []
    result.append(row['TotalWorkbookValue'])
    result.append(row['Pers_Prop'])
    result.append(row['RE_TTV'])
    result.append(row['AV/Unit'])
    result.append(row['Notes'])
    for word in result:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])

        if 'nan' not in k.value:
            k.value = k.value
            result2.append(k)
        else:
            k.value = 'MISSING'
            result2.append(k)
    return result2

def get_title(row):
    thing = str(row['Category'].values)
    thing = thing[3:len(thing)-2]
    return thing

def get_shop_revenue(row):
    revenue = []
    revenue2 = []
    revenue.append(row['Square_Feet'])
    revenue.append(row['Retail_Rent'])
    revenue.append(row['PGI'])
    revenue.append(row['Vacancy'])
    revenue.append(row['Additional Income'])
    revenue.append(row['EGI'])
    for word in revenue:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=2)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        #print k.value[len(k.value)-1]
        if k.value[len(k.value)-1] == ".":
            k.value = k.value[0:len(k.value)-1]
            #print  k.value[0:len(k.value)-2]
        if k.column == 'Additional Income' or k.column == 'Occupancy':
            k.value = str(to_percent(float(k.value), 0))
        elif k.column != 'Suites' and k.column != 'Rooms':
            k.value = "$" + k.value
        if 'nan' not in k.value:
            revenue2.append(k)
        else:
            k.value = 'MISSING'
            revenue2.append(k)
        return revenue2

def get_shop_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Shop_Mgmt'])
    expenses.append(row['Shop_Insurance'])
    expenses.append(row['Shop_Maint'])
    #expenses.append(row['Shop_Replacements'])
    expenses.append(row['Total_Exp ($/SF)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = str(to_percent(float(k.value), 2))
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)   
    return expenses2

def get_mfg_expenses(row):
    expenses = []
    expenses2 = []
    expenses.append(row['Retail_Mgmt'])
    expenses.append(row['Retail_Insurance'])
    expenses.append(row['Retail_Maint'])
    expenses.append(row['Ind_Replacements'])
    expenses.append(row['Total_Exp ($/SF)'])
    for word in expenses:
        if str(word.dtype) == 'float64':
            word = word.round(decimals=4)
        u = str(word.values)
        start = u.find('\'')+1
        end = len(u) - 2
        if start == 0:
            #info2.append(word.name + ": " + u[start+1:len(u)-1] )
            k = tuple(word.name, u[start+1:len(u)-1])
        else:
            #info2.append(word.name + ": " + u[start:end])
            k = tuple(word.name, u[start:end])
        if k.value != ' nan' and 'nan' not in k.value:
            k.value = str(to_percent(float(k.value), 2))
            expenses2.append(k)
        else:
            k.value = 'MISSING'
            expenses2.append(k)
    return expenses2

def get_child_parcels(row):
    try:
        children = row['Child Parcels']
        chi = []
        for thing in children:
            x = thing.split(',')
            for a in x:
                chi.append(a)
        return chi
    except:
        return ['None']
