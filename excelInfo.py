############################################################################################
# Creates the excel file that will be used to hold information. This will allow the 
# program to compare new data against old, and also allow admins to make changes to
# the data on an "as-needed" basis
############################################################################################

#from openpyxl import *
import csv, sqlite3

conn = sqlite3.connect('clanTracker.db')
c = conn.cursor()

def writeDB(clanList):

    # Write the db
    for i in clanList:
        c.execute("INSERT INTO IronBanner VALUES(i)")

    conn.commit()
    conn.close()
    

def createDB():

    # Make the table
    c.execute("CREATE TABLE IF NOT EXISTS IronBanner (Username TEXT, MemberID INTEGER, Char Class TEXT,"+
                "Games INTEGER, Last Game INTEGER, Kills INTEGER, Wins INTEGER, Losses INTEGER"+
                "Deaths INTEGER, KDR REAL, Assists INTEGER, Orbs INTEGER, Objectives INTEGER"+
                "Spree INTEGER)")
    
    # Save the file, then close it
    conn.commit()
    conn.close()

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