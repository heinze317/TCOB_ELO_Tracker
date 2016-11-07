############################################################################################
# Creates the excel file that will be used to hold information. This will allow the 
# program to compare new data against old, and also allow admins to make changes to
# the data on an "as-needed" basis
############################################################################################

import xlrd, xlwt

# Dictionary/Constants
BOOK = 'tcob_tracker.xls'

def createBook():
    ############################################################################################
    # Creates the excel book and sheet
    ############################################################################################

    workbook = xlwt.Workbook()
    workbook.save(BOOK)

def writeInfo(clanList):
    ############################################################################################
    # Saves the data in the spreadsheet 
    ############################################################################################

    # Open the workbook and sheet
    wb = xlwt.open_workbook(BOOK)
    ws = wb.sheet_by_name('ELO')

    row = 1
    col = 0

    # Write the data to the worksheet
    for i in clanList:
        ws.write(row, col, i.displayName)
        row += 1
        col += 1

    wb.save(BOOK)
    
