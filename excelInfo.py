############################################################################################
# Creates the excel file that will be used to hold information. This will allow the 
# program to compare new data against old, and also allow admins to make changes to
# the data on an "as-needed" basis
############################################################################################

#from openpyxl import *
import csv

def writeCSV(clanList):
    ############################################################################################
    # Saves the data to a CSV file, because spreadsheets are hard.... 
    ############################################################################################

    with open('ib.csv', 'w', newline='') as csvfile:
        headers = ['Username', 'MemberID', 'Char Info']
        clanWriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Update the csv file
        for i in clanList:
            clanWriter.writerow([i])        